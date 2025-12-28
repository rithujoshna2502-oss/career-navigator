# Career Navigator - Architecture & Design

## System Overview

Career Navigator is a multi-agent learning platform that:
1. Parses user resumes to assess current skills
2. Generates personalized learning plans for 20+ professions
3. Monitors technology trends and triggers plan updates
4. Tracks daily progress with email reminders
5. Uses AI agents for real-time skill evolution

## Architecture Layers

### 1. Presentation Layer (Frontend)
- **Templates**: `templates/index.html`, `dashboard.html`, `auth.html`
- **Static Assets**: CSS, JavaScript in `static/`
- **Framework**: HTML5 + vanilla JavaScript (no framework dependencies)

### 2. API Layer (Flask)
- **Authentication**: JWT + Flask-Login
- **Security**: CSRF double-submit pattern, password hashing
- **Endpoints**: RESTful API for planning, agents, profiles

### 3. Business Logic Layer
- **Planner** (`planner.py`): Generates daily learning tasks
- **Resume Parser** (`resume_parser.py`): Extracts skills from documents
- **Tech Monitor** (`tech_monitor.py`): Tracks industry trends
- **Agents** (`agents/`): Multi-agent orchestration
- **Advanced Features** (`advanced_features.py`): Analytics & badges

### 4. Data Layer (SQLAlchemy)
- **Database**: SQLite (dev) or PostgreSQL (prod)
- **Models**: User, Resume, Plan, DailyProgress, Progress, TechTrend

### 5. Background Services
- **Orchestrator**: Coordinates agents asynchronously
- **Task Scheduler**: Checks for plan updates periodically
- **Email Service**: Sends daily reminders and alerts

## Multi-Agent System

### Agent Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Request                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────────┐
        │      Orchestrator          │
        │   (Main Coordinator)       │
        └────┬──────┬──────┬─────────┘
             │      │      │
      ┌──────▼─┐  ┌─▼──────┐  ┌──────────┐
      │Skill   │  │Recom-  │  │Monitor   │
      │Assessor│  │mender  │  │(Trends)  │
      └───┬────┘  └──┬─────┘  └────┬─────┘
          │         │              │
          └─────────┴──────────────┘
                    │
                    ▼
            Return: Suggestions
```

### Agent Responsibilities

**SkillAssessor**
- Queries user's latest resume from DB
- Fetches learning progress (tasks completed in last 30 days)
- Calculates skill gaps (required vs. current)
- Returns: current_skills, skill_gaps, proficiency_estimate

**Recommender**
- Takes assessment from SkillAssessor
- Calls tech_monitor for trending tech
- Generates prioritized learning recommendations
- Detects if new technologies should be added to plan
- Returns: must_learn, good_to_learn, emerging_tech

**Monitor**
- Wraps tech_monitor.py functions
- Periodically fetches trending technologies
- Caches trending data (optional)
- Returns: technologies, relevance scores, professions

**Orchestrator**
- Manages other agents
- Runs background loop (threaded)
- Provides API to get suggestions & apply updates
- Coordinates agent communication

## Data Flow Examples

### 1. User Registration & Resume Upload
```
User → /register → Flask App → User model created
User → /upload-resume → resume_parser.py → Resume model saved
                     → SkillAssessor reads resume
                     → Skills extracted & stored
```

### 2. Plan Creation
```
User → /create-plan → planner.generate_daily_plan()
    → Returns: daily_tasks, milestones, technologies
    → Plan model saved with tasks as JSON
    → DailyProgress records created (one per day)
    → Email reminders scheduled
```

### 3. Agent Suggestions (Real-time)
```
GET /api/agent/suggestions
    → Orchestrator.get_suggestions_for_user()
        ├→ SkillAssessor.assess_user()
        │    └→ Query Resume + DailyProgress
        ├→ Recommender.recommend_for_user()
        │    └→ Call tech_monitor.generate_tech_recommendations()
        ├→ Monitor.check_trends()
        │    └→ Call tech_monitor.get_trending_technologies()
        └→ Return aggregated suggestions
```

### 4. Background Plan Update Check
```
TaskScheduler._check_and_update_plans() [hourly]
    → Query plans not checked in 7+ days
    → For each plan:
        └→ tech_monitor.should_update_plan()
        └→ If YES: Mark plan status = 'update_available'
        └→ User sees notification on dashboard
```

## Data Models

### User
```
id (int, PK)
email (str, unique)
name (str)
password_hash (str)
created_at (datetime)
↓ relationships
├─ resumes (Resume)
├─ plans (Plan)
└─ progress (Progress)
```

### Resume
```
id (int, PK)
user_id (int, FK)
filename (str)
file_path (str)
skills (JSON) → ['Python', 'SQL', ...]
experience_level (str) → 'beginner'|'intermediate'|'advanced'
years_of_experience (float)
current_role (str)
education (str)
uploaded_at (datetime)
updated_at (datetime)
```

### Plan
```
id (int, PK)
user_id (int, FK)
resume_id (int, FK)
goal (str) → 'Become Software Engineer'
duration_months (int)
start_date, end_date (datetime)
daily_tasks (JSON) → [{day: 1, task: "...", hours: 2}, ...]
milestones (JSON) → [{week: 2, milestone: "..."}, ...]
technologies (JSON) → ['Python', 'JavaScript', ...]
status (str) → 'active'|'update_pending'|'completed'
version (int) → Track plan updates
last_updated (datetime)
↓ relationship
└─ daily_progress (DailyProgress[])
```

### DailyProgress
```
id (int, PK)
plan_id (int, FK)
day_number (int)
task (str)
planned_date (datetime)
is_completed (bool)
completed_date (datetime, nullable)
hours_spent (float)
notes (str)
```

### Progress
```
id (int, PK)
user_id (int, FK)
total_days_planned (int)
total_days_completed (int)
completion_percentage (float)
last_updated (datetime)
```

### TechTrend
```
id (int, PK)
technology_name (str, unique)
category (str) → 'LLM'|'Framework'|'Tool'
relevance_score (float) → 0-100
last_updated (datetime)
description (str)
learn_resources (JSON) → [links]
```

## Security Considerations

### Authentication
- Passwords hashed with Werkzeug (PBKDF2)
- Flask-Login session management
- User must be authenticated for protected routes

### CSRF Protection
- Double-submit cookie pattern
- X-CSRFToken header required for JSON APIs
- CSRF token unique per session

### Database
- SQLAlchemy ORM prevents SQL injection
- Query parameterization
- In production: use environment variables for secrets

### Communication
- HTTPS required in production
- Secure cookies: `httponly=True`, `samesite='Lax'`
- Session timeout recommended

## Scaling Strategy

### Phase 1: Single Server (Current)
- Flask dev server (or Gunicorn)
- SQLite database
- Threaded background tasks
- Suitable for: < 100 users

### Phase 2: Horizontal Scaling
- Multiple Gunicorn workers
- PostgreSQL database
- Redis for session/cache
- Suitable for: 100-10K users

### Phase 3: Microservices
- Separate API, background job, resume parse services
- Kubernetes orchestration
- Message queue (RabbitMQ/Kafka) for inter-agent communication
- Suitable for: 10K+ users

## Performance Optimizations

### Current
- SQLAlchemy lazy loading (can cause N+1 queries)
- Resume parsing with spaCy + regex (parallelizable)
- Agent suggestions computed on-demand

### Future
- Add database indexing on user_id, plan_id
- Cache trending technologies (Redis, 1 hour TTL)
- Async resume parsing (Celery task)
- Pre-compute agent suggestions (background job)
- Batch email reminders (nightly cron)

## Testing Strategy

### Unit Tests
- `test_planner.py`: Verify plan generation
- `test_agents.py`: Agent initialization and coordination

### Integration Tests (TODO)
- Full user journey (register → upload → plan → progress)
- Email notifications
- Agent coordination

### Load Tests (TODO)
- Concurrent user planning
- Database connection pooling
- Background task throughput

## Monitoring & Observability

### Logs
- Flask app logs (INFO level in prod)
- Background task logs
- Agent operation logs

### Metrics to Track
- API response times
- Plan creation time
- Agent suggestion latency
- Email delivery rate
- Background job queue depth

### Alerts
- High error rates (500s)
- Long response times (>5s)
- Failed background jobs
- Database connection pool exhaustion

## Future Enhancements

### AI Integration
- Replace regex skill extraction with NER (Named Entity Recognition)
- Use LLM to generate better recommendations
- Personalized learning path optimization

### Real-time Features
- WebSocket updates for plan changes
- Live agent suggestions as user types
- Collaborative learning groups

### Mobile App
- React Native or Flutter
- Native push notifications
- Offline-first design

### Analytics
- User learning velocity trends
- Skill adoption rates
- Plan success metrics
- Profession popularity

## Contributing

To extend the system:
1. Add new professions in `planner.py`
2. Implement custom agents in `agents/`
3. Add tests in `tests/`
4. Update README and docs
5. Submit PR with tests passing

---

See [README.md](README.md) for quick start and [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options.
