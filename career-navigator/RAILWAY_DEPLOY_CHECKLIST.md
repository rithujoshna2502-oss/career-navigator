# Railway Deployment Checklist

Quick reference for deploying your Career Navigator to Railway.

## Pre-Deployment Checklist

- [ ] GitHub account created (https://github.com/signup)
- [ ] Railway account created (https://railway.app, use GitHub login)
- [ ] Git installed locally (`git --version`)
- [ ] Project folder has no sensitive data in `.env` (use `.env.example` instead)
- [ ] `Procfile` exists and is correct: `web: gunicorn project.app:app`
- [ ] `requirements.txt` is up-to-date with all dependencies
- [ ] `.gitignore` includes `.env`, `__pycache__/`, `*.db`, `uploads/`

## Quick Deploy Commands

```bash
# 1. Initialize Git (run once)
cd C:\Users\rithu\myprojectenv
git init
git config user.name "Your Name"
git config user.email "your@email.com"
git add .
git commit -m "Initial commit"

# 2. Create GitHub repo at https://github.com/new
# Name: career-navigator
# Visibility: Public

# 3. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/career-navigator.git
git branch -M main
git push -u origin main

# 4. Connect Railway
# - Go to https://railway.app/dashboard
# - Click "+ New Project"
# - Select "Deploy from GitHub repo"
# - Find and deploy career-navigator
# - Add env vars (see RAILWAY_DEPLOYMENT_GUIDE.md)

# 5. Verify deployment
# - Railway assigns public URL
# - Open and test the app

# 6. Auto-deploy (push to main)
git add .
git commit -m "Update feature"
git push origin main
# Railway redeploys automatically
```

## Environment Variables (Set in Railway Dashboard)

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<generate-random-secret>
DATABASE_URL=sqlite:///career_navigator.db
SESSION_COOKIE_SECURE=True
WEBHOOK_SECRET=<generate-random-secret>
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=<your-sendgrid-key>
SENDER_EMAIL=noreply@careernavigator.com
```

## Useful Railway Links

- Dashboard: https://railway.app/dashboard
- Docs: https://docs.railway.app
- Pricing: https://railway.app/pricing
- Support: https://discord.gg/railway

## Common Issues

| Issue | Solution |
|-------|----------|
| Build fails | Check Build Logs; ensure `requirements.txt` is valid |
| App crashes | Check Deployment Logs; verify env vars set |
| Database errors | SQLite works fine for dev; upgrade to PostgreSQL if needed |
| Slow first load | Railway free tier may have slight cold starts |

---

**Status:** Ready to deploy! Follow RAILWAY_DEPLOYMENT_GUIDE.md for detailed steps.
