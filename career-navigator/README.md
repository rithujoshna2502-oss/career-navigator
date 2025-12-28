# Career Navigator — Multi-Agent Career Planner

A Flask application that generates personalized learning plans for various professions and uses a multi-agent system to support real-time skill evolution tracking.

## Features

- **Resume Parsing**: Extract skills and experience level from PDF/TXT resumes
- **AI-Powered Planning**: Generate detailed daily learning plans for 20+ professions
- **Tech Monitoring**: Track trending technologies and suggest plan updates
- **Multi-Agent System**: Real-time skill assessment, recommendations, and monitoring
- **Daily Reminders**: Email notifications for learning tasks
- **Achievement Badges**: Gamification with streaks and milestones
- **Analytics Dashboard**: Track progress and velocity

## Project Structure

```
project/
├── app.py                    # Flask application entry point
├── models.py                 # SQLAlchemy models (User, Plan, Resume, Progress)
├── planner.py               # Learning plan generation engine
├── resume_parser.py         # Resume extraction (PDF/TXT)
├── tech_monitor.py          # Technology trend detection
├── email_service.py         # Email notifications
├── advanced_features.py     # Analytics, badges, recommendations
├── task_scheduler.py        # Background task runner
├── agents/                  # Multi-agent orchestration
│   ├── __init__.py
│   ├── orchestrator.py      # Main orchestrator (coordinates agents)
│   ├── skill_assessor.py    # User skill assessment from resume+progress
│   ├── recommender.py       # Personalized learning recommendations
│   └── monitor.py           # Technology trend wrapper
├── static/                  # Frontend assets
├── templates/               # HTML templates
├── tests/
│   ├── test_planner.py      # Unit tests for planner
│   └── test_agents.py       # Unit tests for agents
└── uploads/                 # Uploaded resume files
```

## Multi-Agent Architecture

The system uses four cooperating agents:

1. **SkillAssessor**: Evaluates user's current skills from resume and learning progress
2. **Recommender**: Generates personalized learning recommendations based on skill gaps
3. **Monitor**: Detects emerging technologies relevant to career goals
4. **Orchestrator**: Coordinates agents, manages background tasks, provides API

### Agent Flow

```
User Request
    ↓
Orchestrator.get_suggestions_for_user()
    ├→ SkillAssessor.assess_user()  [Query resume + progress]
    ├→ Recommender.recommend_for_user()  [Generate prioritized skills]
    ├→ Monitor.check_trends()  [Fetch trending tech]
    ↓
Return: Assessment + Recommendations
```

## Quick Start

### 1. Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r project/requirements.txt
pip install pytest
```

### 2. Run the App

```bash
set FLASK_APP=project.app
set DATABASE_URL=sqlite:///career_navigator.db
flask run
```

The app will start at `http://localhost:5000` and automatically start background services (orchestrator, task scheduler).

### 3. Run Tests

```bash
$env:PYTHONPATH = 'C:\Users\rithu\myprojectenv\project'
pytest -q project/tests/
```

## API Endpoints

### Authentication
- `POST /register` — Register a new user
- `POST /login` — Login user
- `GET /logout` — Logout user

### Core Features
- `POST /api/upload-resume` — Upload and parse resume
- `POST /api/create-plan` — Generate learning plan
- `GET /` — Dashboard (requires login)

### Agent API
- `GET /api/agent/suggestions` — Get personalized suggestions (requires login)
- `POST /api/agent/apply-update` — Apply recommended plan update (requires login)

### CSRF Protection
- `GET /api/get-csrf-token` — Get CSRF token for double-submit pattern
- `POST /api/test-csrf` — Test CSRF validation

## Configuration

Set these environment variables:

```bash
# Flask
FLASK_ENV=development
FLASK_APP=project.app
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///career_navigator.db
# Or: postgresql://user:pass@localhost/career_nav

# Email (optional, for reminders)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-key
SENDER_EMAIL=noreply@careernavigator.com

# Agents
AGENT_POLL_INTERVAL=60  # Seconds
TASK_SCHEDULER_INTERVAL=3600  # Seconds (1 hour)

# Session
SESSION_COOKIE_SECURE=False  # Set to True in production
```

## Production Deployment

For production:

1. **Database**: Replace SQLite with PostgreSQL
   ```bash
   pip install psycopg2-binary
   export DATABASE_URL=postgresql://user:pass@host/dbname
   ```

2. **Task Queue**: Replace threaded scheduler with Celery + Redis
   ```bash
   pip install celery redis
   ```

3. **Email**: Configure SendGrid or another SMTP service

4. **Web Server**: Use Gunicorn or uWSGI
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 'project.app:app'
   ```

5. **Background Workers**:
   ```bash
   celery -A project.tasks worker -l info
   ```

## Testing

Run all tests:
```bash
pytest -q project/tests/
```

Run specific tests:
```bash
pytest -q project/tests/test_planner.py::test_generate_daily_plan_day_indexing_and_length
pytest -q project/tests/test_agents.py::test_orchestrator_initialization
```

## CI/CD

GitHub Actions workflow is configured in `.github/workflows/ci.yml`. On each push/PR:
- Install dependencies
- Run pytest (currently tests planner and agents)

To add more CI checks, edit the workflow file.

## Extending the System

### Adding a New Profession

Edit `project/planner.py` and add to `PROFESSION_PATHS`:

```python
'your_profession': {
    'duration_months': 6,
    'skills_required': ['Skill1', 'Skill2', ...],
    'daily_distribution': {
        'weeks_1_2': {'focus': 'Topic', 'daily_hours': 3},
        ...
    },
    'milestones': [...]
}
```

### Adding a Custom Agent

1. Create `project/agents/custom_agent.py`
2. Implement the agent class
3. Wire it into `Orchestrator` in `project/agents/orchestrator.py`

## Known Limitations

- Task scheduler runs on a single thread (use Celery for production)
- Email service requires proper SMTP/SendGrid config
- Resume parsing is regex-based (can be improved with ML)
- No user notification UI for plan updates yet

## License

MIT

## Support

For issues or questions, open an issue in the repository.

