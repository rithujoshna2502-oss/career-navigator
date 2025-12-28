# Career Navigator - Deployment Guide

## Quick Deploy Options

### 🚀 Railway (Recommended for Quick Start)

1. **Push to GitHub**
   ```bash
   git init && git add . && git commit -m "Initial"
   git remote add origin https://github.com/YOUR/repo.git
   git push -u origin main
   ```

2. **Deploy on Railway**
   - Go to https://railway.app/dashboard
   - "New Project" → "Deploy from GitHub"
   - Connect repo (Railway auto-detects Procfile)
   - Set environment variables:
     ```
     SECRET_KEY=<generate-strong-key>
     FLASK_ENV=production
     MAIL_PASSWORD=<sendgrid-api-key>
     SESSION_COOKIE_SECURE=True
     ```
   - Click Deploy (live in 2-5 min)

---

## Local Development

### Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r project/requirements.txt
```

### Run
```bash
set FLASK_APP=project.app
set DATABASE_URL=sqlite:///career_navigator.db
flask run
```

---

## Docker Deployment

### Build & Run
```bash
docker build -t career-nav .
docker run -e SECRET_KEY=your-key -e DATABASE_URL=postgresql://... -p 5000:5000 career-nav
```

---

## AWS Deployment

### EC2 + RDS
1. Launch t3.small Ubuntu 22.04 instance
2. Create RDS PostgreSQL database
3. SSH and deploy:
   ```bash
   sudo apt update && sudo apt install -y python3-pip python3-venv git
   git clone <repo>
   cd myprojectenv && python3 -m venv .venv
   source .venv/bin/activate
   pip install -r project/requirements.txt gunicorn
   export DATABASE_URL=postgresql://user:pass@rds-host:5432/db
   export SECRET_KEY=...
   gunicorn -w 4 -b 0.0.0.0:5000 project.app:app
   ```

### ECS + RDS
- Push Docker image to ECR
- Create ECS task definition (point to ECR)
- Attach RDS database
- Create ALB for routing

---

## Google Cloud Run

```bash
gcloud run deploy career-navigator \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars DATABASE_URL=your-cloud-sql-url,SECRET_KEY=your-key
```

---

## Production Checklist

- [ ] Use PostgreSQL (not SQLite)
- [ ] Set strong `SECRET_KEY`
- [ ] Enable `SESSION_COOKIE_SECURE=True`
- [ ] Configure email service
- [ ] Setup HTTPS/SSL
- [ ] Enable logging (Sentry, CloudWatch)
- [ ] Setup database backups
- [ ] Configure Redis + Celery (optional, for scales)
- [ ] Add health check endpoint
- [ ] Setup monitoring & alerts

### Email Setup (SendGrid)

1. Sign up at https://sendgrid.com (free: 100/day)
2. Get API key from Settings → API Keys
3. Set env vars:
   ```
   MAIL_PASSWORD=<api-key>
   MAIL_USERNAME=apikey
   SENDER_EMAIL=noreply@yourdomain.com
   ```

### Add Health Check

```python
@app.route('/health')
def health():
    return {'status': 'ok'}, 200
```

---

## Scaling to Production

When ready for high traffic:

1. **Database**: Switch to managed PostgreSQL
2. **Cache**: Add Redis for sessions/caching
3. **Tasks**: Integrate Celery + Redis for background jobs
4. **Web Server**: Use Gunicorn/uWSGI with multiple workers
5. **Monitoring**: Add Sentry, DataDog, or CloudWatch
6. **CDN**: Serve static files from CloudFront/Cloudflare

### Celery Setup

```bash
pip install celery redis
celery -A project.tasks worker -l info
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection fails | Verify `DATABASE_URL`, check security groups |
| Email not sending | Check SMTP creds, verify firewall allows port 587 |
| Static files 404 | Ensure Flask serves from correct path |
| High memory usage | Scale workers, check for memory leaks |
| Background tasks slow | Add Redis caching, scale Celery workers |

---

For detailed setup instructions, see [README.md](README.md).
- Gmail: `smtp.gmail.com:587`
- Outlook: `smtp-mail.outlook.com:587`

---

## 🎯 Current Status
- [x] Core app working
- [x] CSRF protection
- [x] Resume upload & parsing
- [x] Day-by-day plan generation
- [ ] Cloud deployment (NEXT)
- [ ] Email notifications
- [ ] Enhanced PDF parser
- [ ] Social features
- [ ] Mobile app
- [ ] AI recommendations
- [ ] Analytics dashboard
