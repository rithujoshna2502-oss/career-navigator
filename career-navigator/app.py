from flask import Flask, render_template, request, jsonify, redirect, url_for, session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf.csrf import CSRFProtect, CSRFError
from flask_wtf.csrf import generate_csrf
from werkzeug.utils import secure_filename
from functools import wraps
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import custom modules
from models import db, User, Resume, Plan, DailyProgress, Progress
from resume_parser import parse_txt_resume, parse_pdf_resume
from planner import generate_daily_plan
from tech_monitor import detect_new_technologies, should_update_plan, generate_tech_recommendations, get_technology_update_summary
from email_service import mail, send_daily_reminder_email, send_tech_update_alert_email, send_plan_update_confirmation_email
# Agents orchestrator
from agents.orchestrator import Orchestrator
# Background task scheduler
from task_scheduler import TaskScheduler
from security_utils import sanitize_text, sanitize_list, verify_hmac_signature
from security_utils import verify_api_key
import json
import base64

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '8901c3ae8e48810b721c0e71c01d386dfe38b458')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///career_navigator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
# Session cookie hardening
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'

# Email configuration for notifications
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.sendgrid.net')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'apikey')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SENDER_EMAIL', 'noreply@careernavigator.com')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

# Create upload folder if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Initialize database
db.init_app(app)

# Initialize Flask-Mail for email notifications
mail.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize CSRF protection (only for forms, not JSON APIs using custom double-submit)
csrf = CSRFProtect()
csrf.init_app(app)


# Security: set default security headers and CSP
@app.after_request
def set_security_headers(response):
    # Content Security Policy - adjust as needed for your app's external resources
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self' https://api.github.com http://127.0.0.1:5000 ws:; "
        "frame-ancestors 'none';"
    )
    response.headers.setdefault('Content-Security-Policy', csp)
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('X-Frame-Options', 'DENY')
    response.headers.setdefault('Referrer-Policy', 'no-referrer')
    # Enforce HSTS for secure deployments
    if app.config.get('SESSION_COOKIE_SECURE'):
        response.headers.setdefault('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload')
    return response


# Create a global orchestrator instance; started on first request
orchestrator = Orchestrator(poll_interval=int(os.getenv('AGENT_POLL_INTERVAL', '60')))

# Create task scheduler for background plan update checks
task_scheduler = TaskScheduler(app, interval=int(os.getenv('TASK_SCHEDULER_INTERVAL', '3600')))


def _start_background_services():
    """Start background services on app startup."""
    try:
        orchestrator.start()
        task_scheduler.start()
    except Exception as e:
        app.logger.error(f"Error starting background services: {e}")


# For Flask 2.0+, use app context instead of before_first_request
with app.app_context():
    db.create_all()
    # Start services after app context is ready
    _start_background_services()


# Helpers: decorators to enforce CSRF via double-submit (header matches cookie)
def require_csrf_header():
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            header = request.headers.get('X-CSRFToken') or request.headers.get('X-CSRF-Token')
            cookie = request.cookies.get('csrf_token')
            if not header or not cookie or header != cookie:
                return jsonify({'error': 'CSRF token missing or invalid'}), 400
            return f(*args, **kwargs)
        return wrapped
    return decorator


def require_json_and_csrf(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            header = request.headers.get('X-CSRFToken') or request.headers.get('X-CSRF-Token')
            cookie = request.cookies.get('csrf_token')
            if not header or not cookie or header != cookie:
                return jsonify({'error': 'CSRF token missing or invalid'}), 400

            data = request.get_json()
            ok, err = require_json_fields(data, required_fields or {})
            if not ok:
                return jsonify({'error': err}), 400

            return f(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/api/get-csrf-token', methods=['GET'])
def get_csrf_token():
    """Return a fresh CSRF token and set it as a cookie for double-submit pattern."""
    token = generate_csrf()
    resp = jsonify({'csrf_token': token})
    # Cookie must be readable by JS for double-submit; set appropriate flags in production
    resp.set_cookie('csrf_token', token, samesite='Lax')
    return resp


@app.route('/api/test-csrf', methods=['POST'])
@csrf.exempt
def test_csrf():
    """Temporary test endpoint to validate CSRF double-submit behavior without login."""
    # Use the same check as require_csrf_header to demonstrate failures to the client
    header = request.headers.get('X-CSRFToken') or request.headers.get('X-CSRF-Token')
    cookie = request.cookies.get('csrf_token')
    if not header or not cookie or header != cookie:
        return jsonify({'error': 'CSRF token missing or invalid', 'header': header, 'cookie': cookie}), 400
    return jsonify({'success': True, 'message': 'CSRF validated'}), 200


# Simple JSON validation helpers
def require_json_fields(data, required_fields):
    if not data:
        return False, 'Invalid or missing JSON body'
    for field, ftype in required_fields.items():
        if field not in data:
            return False, f'Missing field: {field}'
        if ftype and not isinstance(data.get(field), ftype):
            return False, f'Invalid type for {field}: expected {ftype.__name__}'
    return True, None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    if current_user.is_authenticated:
        token = generate_csrf()
        resp = make_response(render_template("dashboard.html", csrf_token=token))
        # Set readable cookie for double-submit CSRF pattern (adjust flags in production)
        resp.set_cookie('csrf_token', token, samesite='Lax')
        return resp
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
@csrf.exempt
def register():
    """Register a new user account"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            password = data.get('password', '')
            password_confirm = data.get('password_confirm', '')
            
            # Validation
            if not name or len(name) < 2:
                return jsonify({'error': 'Name must be at least 2 characters'}), 400
            
            if not email or '@' not in email:
                return jsonify({'error': 'Invalid email address'}), 400
            
            if not password or len(password) < 6:
                return jsonify({'error': 'Password must be at least 6 characters'}), 400
            
            if password != password_confirm:
                return jsonify({'error': 'Passwords do not match'}), 400
            
            # Check if user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({'error': 'Email already registered'}), 400
            
            # Create new user
            user = User(name=name, email=email)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Log user in
            login_user(user)
            session.permanent = True
            session.modified = True
            
            return jsonify({'success': True, 'message': 'Registration successful!'}), 201
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template("auth.html", page='register')


@app.route("/login", methods=['GET', 'POST'])
@csrf.exempt
def login():
    """Login to user account"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            
            email = data.get('email', '').strip()
            password = data.get('password', '')
            
            if not email or not password:
                return jsonify({'error': 'Email and password required'}), 400
            
            # Find user by email
            user = User.query.filter_by(email=email).first()
            
            if not user or not user.check_password(password):
                return jsonify({'error': 'Invalid email or password'}), 401
            
            # Log user in
            login_user(user)
            session.permanent = True
            session.modified = True
            
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template("auth.html", page='login')


@app.route("/logout")
@login_required
def logout():
    """Logout user"""
    logout_user()
    return redirect(url_for('login'))


@app.route("/api/upload-resume", methods=['POST'])
@login_required
@csrf.exempt
@require_csrf_header()
def upload_resume():
    """Handle resume upload and parsing"""
    try:
        # Check if file was uploaded
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .txt and .pdf files are allowed'}), 400
        
        # Get current user
        user = current_user
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse resume based on file type
        file_ext = filename.rsplit('.', 1)[1].lower()
        if file_ext == 'pdf':
            parsed_data = parse_pdf_resume(filepath)
        else:
            parsed_data = parse_txt_resume(filepath)
        
        # Save resume to database
        # Sanitize parsed text fields before saving to DB to avoid any injected HTML
        sanitized_skills = sanitize_list(parsed_data.get('skills', []))
        resume = Resume(
            user_id=user.id,
            filename=file.filename,
            file_path=filepath,
            skills=sanitized_skills,
            experience_level=sanitize_text(parsed_data.get('experience_level', 'beginner')),
            years_of_experience=int(parsed_data.get('years_of_experience', 0) or 0),
            current_role=sanitize_text(parsed_data.get('current_role', 'Not specified')),
            education=sanitize_text(parsed_data.get('education', 'Not specified'))
        )
        db.session.add(resume)
        db.session.commit()
        
        session['user_id'] = user.id
        session['resume_id'] = resume.id
        
        return jsonify({
            'success': True,
            'resume_id': resume.id,
            'user_id': user.id,
            'parsed_data': parsed_data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/create-plan", methods=['POST'])
@login_required
@csrf.exempt
@require_json_and_csrf({'resume_id': None, 'goal': None, 'duration_months': None})
def create_plan():
    """Create a personalized day-by-day learning plan"""
    try:
        data = request.get_json()
        
        resume_id = data.get('resume_id')
        goal = data.get('goal')  # "Become a Software Engineer"
        duration_months = int(data.get('duration_months', 6))
        
        # Get resume and verify ownership
        resume = Resume.query.get(resume_id)
        if not resume:
            return jsonify({'error': 'Resume not found'}), 404
        
        if resume.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        user = current_user
        
        # Generate daily plan
        plan_content = generate_daily_plan(
            profession=goal,
            duration_months=duration_months,
            current_skills=resume.skills or [],
            experience_level=resume.experience_level
        )
        
        # Create plan record
        start_date = datetime.now()
        end_date = start_date + timedelta(days=plan_content['total_days'])
        
        plan = Plan(
            user_id=user.id,
            resume_id=resume.id,
            goal=goal,
            duration_months=duration_months,
            start_date=start_date,
            end_date=end_date,
            daily_tasks=plan_content['daily_tasks'],
            milestones=plan_content['milestones'],
            technologies=plan_content['technologies']
        )
        db.session.add(plan)
        db.session.commit()
        
        # Create daily progress records
        for task in plan_content['daily_tasks']:
            planned_date = start_date + timedelta(days=task['day'])
            daily_progress = DailyProgress(
                plan_id=plan.id,
                day_number=task['day'],
                task=task['task'],
                planned_date=planned_date
            )
            db.session.add(daily_progress)
        
        # Create progress tracker
        progress = Progress(
            user_id=user.id,
            total_days_planned=plan_content['total_days']
        )
        db.session.add(progress)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'plan_id': plan.id,
            'plan_data': {
                'goal': goal,
                'duration_months': duration_months,
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'milestones': plan_content['milestones'],
                'total_tasks': len(plan_content['daily_tasks'])
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/suggestions', methods=['GET'])
@login_required
def agent_suggestions():
    """Get personalized learning suggestions from the orchestrator."""
    try:
        user = current_user
        suggestions = orchestrator.get_suggestions_for_user(user.id)
        return jsonify({'success': True, 'suggestions': suggestions}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/agent/apply-update', methods=['POST'])
@login_required
@csrf.exempt
@require_json_and_csrf({'plan_id': None, 'new_technologies': list})
def agent_apply_update():
    """Apply an agent-recommended update to the user's plan."""
    try:
        data = request.get_json()
        user = current_user
        plan_id = data.get('plan_id')
        new_technologies = data.get('new_technologies', [])
        
        # Verify user owns the plan
        from models import Plan
        plan = Plan.query.get(plan_id)
        if not plan or plan.user_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        update_payload = {
            'plan_id': plan_id,
            'new_technologies': new_technologies
        }
        result = orchestrator.apply_update(user.id, update_payload)
        return jsonify({'success': True, 'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/webhook/example', methods=['POST'])
def webhook_example():
    """Example webhook endpoint demonstrating HMAC SHA256 signature verification.

    - Configure your external webhook sender to HMAC-SHA256 the raw body with a shared secret
      and send the hex digest in header `X-Signature`.
    - Set `WEBHOOK_SECRET` in your environment for verification.
    """
    try:
        secret = os.getenv('WEBHOOK_SECRET')
        signature = request.headers.get('X-Signature') or request.headers.get('X-Hub-Signature')
        raw = request.get_data() or b''

        if not verify_hmac_signature(secret or '', raw, signature or ''):
            return jsonify({'error': 'Invalid signature'}), 401

        payload = None
        try:
            payload = request.get_json(force=False, silent=True)
        except Exception:
            payload = None

        # Process the webhook safely here (example: enqueue for background processing)
        return jsonify({'success': True, 'received': bool(payload)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/admin/users', methods=['GET'])
@csrf.exempt
def admin_list_users():
    """Admin endpoint example: list all users (protected by API key).
    
    Requires Authorization header: `Bearer <API_KEY>` or `X-API-Key: <API_KEY>`.
    Set API_ADMIN_KEY in environment for protection.
    """
    try:
        api_key = os.getenv('API_ADMIN_KEY', 'dev-key-change-in-production')
        
        # Verify API key
        if not verify_api_key(dict(request.headers), api_key):
            return jsonify({'error': 'Unauthorized: invalid or missing API key'}), 401
        
        # Fetch all users (admin only)
        users = User.query.all()
        user_data = [{
            'id': u.id,
            'name': u.name,
            'email': u.email,
            'created_at': u.created_at.isoformat()
        } for u in users]
        
        return jsonify({
            'success': True,
            'total_users': len(users),
            'users': user_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/plan/<int:plan_id>")
@login_required
def get_plan(plan_id):
    """Get plan details with daily tasks"""
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        if plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get all daily tasks for this plan
        daily_tasks = DailyProgress.query.filter_by(plan_id=plan_id).all()
        
        # Calculate progress
        completed_tasks = sum(1 for task in daily_tasks if task.is_completed)
        total_tasks = len(daily_tasks)
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        return jsonify({
            'plan': {
                'id': plan.id,
                'goal': plan.goal,
                'duration_months': plan.duration_months,
                'start_date': plan.start_date.isoformat(),
                'end_date': plan.end_date.isoformat(),
                'milestones': plan.milestones,
                'technologies': plan.technologies,
                'total_days': total_tasks,
                'completed_days': completed_tasks,
                'completion_percentage': completion_percentage
            },
            'daily_tasks': [{
                'id': task.id,
                'day': task.day_number,
                'task': task.task,
                'completed': task.is_completed,
                'date': task.planned_date.isoformat(),
                'hours_spent': task.hours_spent,
                'notes': task.notes
            } for task in daily_tasks[:30]]  # Return first 30 tasks
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/plan/<int:plan_id>/all-tasks")
@login_required
def get_all_tasks(plan_id):
    """Get all daily tasks for a plan (paginated)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 20
        
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        if plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get paginated tasks
        tasks = DailyProgress.query.filter_by(plan_id=plan_id).paginate(
            page=page, 
            per_page=per_page
        )
        
        return jsonify({
            'total_tasks': tasks.total,
            'current_page': page,
            'total_pages': tasks.pages,
            'daily_tasks': [{
                'id': task.id,
                'day': task.day_number,
                'task': task.task,
                'completed': task.is_completed,
                'date': task.planned_date.isoformat(),
                'hours_spent': task.hours_spent,
                'notes': task.notes,
                'completed_date': task.completed_date.isoformat() if task.completed_date else None
            } for task in tasks.items]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/update-progress/<int:daily_progress_id>", methods=['POST'])
@login_required
@csrf.exempt
@require_json_and_csrf({'is_completed': None})
def update_progress(daily_progress_id):
    """Mark a daily task as completed and track hours/notes"""
    try:
        data = request.get_json()
        
        progress = DailyProgress.query.get(daily_progress_id)
        if not progress:
            return jsonify({'error': 'Progress not found'}), 404
        
        # Verify user owns this plan
        if progress.plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update task progress
        is_completed = data.get('is_completed', False)
        progress.is_completed = is_completed
        progress.hours_spent = float(data.get('hours_spent', 0))
        progress.notes = data.get('notes', '')
        
        if is_completed and not progress.completed_date:
            progress.completed_date = datetime.now()
        elif not is_completed:
            progress.completed_date = None
        
        db.session.commit()
        
        # Update overall plan progress
        plan = progress.plan
        completed_tasks = DailyProgress.query.filter_by(plan_id=plan.id, is_completed=True).count()
        total_tasks = DailyProgress.query.filter_by(plan_id=plan.id).count()
        completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        user_progress = Progress.query.filter_by(user_id=plan.user_id).first()
        if user_progress:
            user_progress.total_days_completed = completed_tasks
            user_progress.completion_percentage = completion_percentage
            user_progress.last_updated = datetime.now()
            db.session.commit()
        
        # Get next upcoming task
        next_task = DailyProgress.query.filter_by(
            plan_id=plan.id, 
            is_completed=False
        ).order_by(DailyProgress.day_number).first()
        
        return jsonify({
            'success': True,
            'completion_percentage': completion_percentage,
            'completed_tasks': completed_tasks,
            'total_tasks': total_tasks,
            'next_task': {
                'id': next_task.id,
                'day': next_task.day_number,
                'task': next_task.task
            } if next_task else None
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/check-tech-updates/<int:plan_id>", methods=['GET'])
@login_required
def check_tech_updates(plan_id):
    """Check if new technologies emerged for a plan"""
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        if plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Calculate days since plan creation
        days_since = (datetime.now() - plan.created_at).days
        
        # Check if plan should be updated
        update_info = should_update_plan(
            plan.technologies or [],
            plan.goal,
            days_since_creation=days_since
        )
        
        return jsonify({
            'plan_id': plan_id,
            'should_update': update_info['should_update'],
            'reason': update_info['reason'],
            'days_since_creation': days_since,
            'new_technologies': update_info.get('new_technologies', []),
            'urgency': update_info.get('urgency', 'none'),
            'checked_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/tech-recommendations/<int:plan_id>", methods=['GET'])
@login_required
def get_tech_recommendations(plan_id):
    """Get technology recommendations for a plan"""
    try:
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        if plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        recommendations = generate_tech_recommendations(
            plan.goal,
            plan.technologies or []
        )
        
        return jsonify({
            'plan_id': plan_id,
            'profession': plan.goal,
            'recommendations': {
                'must_learn': recommendations['must_learn'],
                'good_to_learn': recommendations['good_to_learn'],
                'emerging': recommendations['emerging']
            },
            'total_recommendations': {
                'must_learn': len(recommendations['must_learn']),
                'good_to_learn': len(recommendations['good_to_learn']),
                'emerging': len(recommendations['emerging'])
            },
            'generated_at': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/update-plan-tech/<int:plan_id>", methods=['POST'])
@login_required
@csrf.exempt
@require_json_and_csrf({'technologies': list})
def update_plan_tech(plan_id):
    """Update plan with new technologies"""
    try:
        data = request.get_json()
        
        plan = Plan.query.get(plan_id)
        if not plan:
            return jsonify({'error': 'Plan not found'}), 404
        
        if plan.user_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        old_technologies = plan.technologies or []
        new_technologies = data.get('technologies', [])
        
        # Update plan
        plan.technologies = new_technologies
        plan.last_updated = datetime.now()
        plan.version = (plan.version or 1) + 1
        plan.status = 'updated'
        
        # Log the change
        summary = get_technology_update_summary(old_technologies, new_technologies)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'plan_id': plan_id,
            'new_version': plan.version,
            'changes': summary,
            'message': f"Plan updated with {summary['added_count']} new technologies"
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/trending-tech", methods=['GET'])
def get_trending_tech():
    """Get globally trending technologies"""
    try:
        from tech_monitor import get_trending_technologies
        
        profession = request.args.get('profession')
        min_relevance = int(request.args.get('min_relevance', 75))
        
        trending = get_trending_technologies(profession, min_relevance)
        
        return jsonify({
            'profession': profession or 'all',
            'min_relevance': min_relevance,
            'trending_technologies': trending,
            'total': len(trending),
            'last_updated': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/user-info")
@login_required
def get_user_info():
    """Get current logged-in user information"""
    try:
        return jsonify({
            'success': True,
            'id': current_user.id,
            'name': current_user.name,
            'email': current_user.email,
            'created_at': current_user.created_at.isoformat()
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/send-test-email", methods=['POST'])
@login_required
def send_test_email():
    """Send a test email to verify email configuration"""
    try:
        user = current_user
        
        # Check if email is configured
        if not app.config.get('MAIL_PASSWORD'):
            # Development mode: just log to console
            print(f"\n📧 TEST EMAIL (DEV MODE - Not sending)")
            print(f"To: {user.email}")
            print(f"Subject: 🎯 Daily Learning Reminder - Career Growth")
            print(f"Body: Test email from Career Navigator")
            print(f"Note: Configure MAIL_PASSWORD in .env to enable actual email sending\n")
            
            return jsonify({
                'success': True, 
                'message': 'Test email logged to console (dev mode). Configure MAIL_PASSWORD to send actual emails.',
                'dev_mode': True
            }), 200
        
        result = send_daily_reminder_email(
            user_email=user.email,
            user_name=user.name,
            plan_goal="Career Growth",
            today_task="Review your learning plan and confirm email service is working",
            duration_months=6
        )
        if result:
            return jsonify({'success': True, 'message': 'Test email sent successfully!'}), 200
        else:
            return jsonify({'error': 'Failed to send email. Check your email configuration.'}), 500
    except Exception as e:
        print(f"Email error: {str(e)}")
        return jsonify({'error': f'Email configuration error: {str(e)}'}), 500


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return jsonify({'error': 'CSRF token missing or invalid', 'description': str(e)}), 400


@app.after_request
def set_security_headers(response):
    # Basic security headers; tweak CSP for your app in production
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer-when-downgrade'
    response.headers['Permissions-Policy'] = 'geolocation=()'
    # Content-Security-Policy minimal default (adjust for inline scripts/assets)
    response.headers.setdefault('Content-Security-Policy', "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';")
    return response


if __name__ == '__main__':
    # Production: debug=False, local: debug=True
    is_production = os.getenv('ENVIRONMENT') == 'production'
    app.run(debug=not is_production, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
