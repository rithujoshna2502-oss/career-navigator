# Quick Start Guide

## 5-Minute Setup (Local)

### 1. Clone & Setup
```bash
# Navigate to project folder
cd myprojectenv

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r project/requirements.txt
```

### 2. Run the App
```bash
set FLASK_APP=project.app
set FLASK_ENV=development
flask run
```

Visit `http://localhost:5000` and register!

---

## Try It Out

### 1. Register a User
- Click "Register" on homepage
- Fill in name, email, password
- Click "Sign up"

### 2. Upload a Resume
- Paste or upload a resume (`.txt` or `.pdf`)
- Click "Parse Resume"
- See extracted skills!

### 3. Generate a Learning Plan
- Select target role (e.g., "Software Engineer")
- Choose duration (default: 6 months)
- Click "Create Plan"
- View your daily tasks

### 4. View Agent Suggestions
- Go to Dashboard → "Get Suggestions"
- AI agents will assess your skills
- See recommendations for improvement

### 5. Check Progress
- Mark tasks as complete
- View analytics (velocity, badges, completion %)

---

## Testing

### Run Tests
```bash
# Set Python path
$env:PYTHONPATH = 'C:\Users\rithu\myprojectenv\project'

# Run all tests
pytest -q project/tests/

# Run specific test
pytest -q project/tests/test_planner.py::test_generate_daily_plan_day_indexing_and_length
```

### Expected Output
```
....... passed
```

---

## Common Tasks

### Generate a New Learning Plan
```bash
flask shell
>>> from project.models import db, User, Plan
>>> user = User.query.filter_by(email='user@example.com').first()
>>> # Create plan...
```

### Check Trending Technologies
```bash
python -c "from project.tech_monitor import get_trending_technologies; print(get_trending_technologies('Software Engineer'))"
```

### Run Background Tasks Manually
```bash
from project.task_scheduler import TaskScheduler
scheduler = TaskScheduler(app, interval=1)
scheduler._check_and_update_plans()
```

### Send Test Email
```bash
flask shell
>>> from project.email_service import send_daily_reminder_email
>>> send_daily_reminder_email('user@example.com', 'John', 'AI Engineer', 'Learn PyTorch basics', 6)
```

---

## Configuration

Environment variables (optional, have defaults):

```bash
# App
FLASK_ENV=development  # or production
SECRET_KEY=dev-secret-key

# Database
DATABASE_URL=sqlite:///career_navigator.db
# Or: postgresql://user:pass@localhost/dbname

# Email (optional)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-key
SENDER_EMAIL=noreply@careernavigator.com

# Agents
AGENT_POLL_INTERVAL=60  # seconds
TASK_SCHEDULER_INTERVAL=3600  # seconds
```

---

## Project Structure Overview

```
project/
├── app.py                      # Main Flask app
├── models.py                   # Database models
├── planner.py                  # Plan generation
├── resume_parser.py            # Resume extraction
├── tech_monitor.py             # Technology trends
├── email_service.py            # Email notifications
├── advanced_features.py        # Analytics & badges
├── task_scheduler.py           # Background jobs
├── agents/
│   ├── orchestrator.py        # Main agent coordinator
│   ├── skill_assessor.py      # Skill assessment
│   ├── recommender.py         # Recommendations
│   └── monitor.py             # Tech monitoring
├── templates/                  # HTML templates
├── static/                     # CSS, JS
├── tests/                      # Unit tests
└── uploads/                    # Resume files
```

---

## Troubleshooting

### Port 5000 already in use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Database locked
```bash
# Delete and recreate
rm career_navigator.db
flask run  # Will recreate on startup
```

### Import errors
```bash
# Ensure PYTHONPATH is set
$env:PYTHONPATH = 'C:\Users\rithu\myprojectenv\project'
```

### Resume not parsing
- Ensure file is `.pdf` or `.txt`
- Text must be readable (not scanned image)
- Check `uploads/` folder for extracted file

---

## Next Steps

1. **Deploy**: See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway/AWS/Docker options
2. **Extend**: Add professions in `planner.py`, custom agents in `agents/`
3. **Integrate**: Wire to your own resume parsing, email service, etc.
4. **Scale**: Add Redis/Celery for high-traffic production

---

For full documentation, see [README.md](README.md) and [ARCHITECTURE.md](ARCHITECTURE.md).
