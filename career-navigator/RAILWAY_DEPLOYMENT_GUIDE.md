# Deploy Career Navigator to Railway (Free Tier)

Railway is the recommended free hosting platform for your Career Navigator app. It provides:
- ✓ Persistent public URL (stays up 24/7)
- ✓ Free tier: $5 USD monthly credit (usually sufficient for dev apps)
- ✓ Auto-deploys on Git push
- ✓ Easy environment variable management
- ✓ Supports Python/Flask out of the box
- ✓ PostgreSQL & Redis add-ons available (optional)

## Prerequisites

1. **GitHub Account** (required for Railway integration)
   - Sign up: https://github.com/signup

2. **Railway Account** (free)
   - Sign up: https://railway.app (use GitHub login)

3. **Git installed locally**
   - Verify: `git --version`
   - Install if needed: https://git-scm.com/download/win

4. **Project ready to deploy**
   - `Procfile` configured ✓
   - `.env.example` with all required vars ✓
   - `requirements.txt` updated ✓

## Step-by-Step Deployment

### Step 1: Initialize Git repository locally

```bash
cd C:\Users\rithu\myprojectenv
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: Career Navigator app"
```

### Step 2: Create a GitHub repository

1. Go to https://github.com/new
2. Repository name: `career-navigator`
3. Description: `Multi-agent career navigation and skill tracking system`
4. Visibility: **Public** (required for free Railway deployment)
5. Click **Create repository**
6. Copy the HTTPS URL (e.g., `https://github.com/YOUR_USERNAME/career-navigator.git`)

### Step 3: Push code to GitHub

```bash
cd C:\Users\rithu\myprojectenv
git remote add origin https://github.com/YOUR_USERNAME/career-navigator.git
git branch -M main
git push -u origin main
```

(If prompted for credentials, use GitHub personal access token or web login)

### Step 4: Connect Railway to GitHub

1. Go to https://railway.app/dashboard
2. Click **+ New Project**
3. Select **Deploy from GitHub repo**
4. Authorize Railway with your GitHub account (one-time)
5. Search for and select `career-navigator` repo
6. Click **Deploy**

Railway will auto-detect the Python app, install dependencies, and run the `Procfile` command.

### Step 5: Configure Environment Variables

After deployment starts:

1. In Railway dashboard, click your project
2. Click the **Variables** tab
3. Add the following environment variables (copy from `.env`):

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=<your-secret-key>
DATABASE_URL=sqlite:///career_navigator.db
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=<your-sendgrid-api-key>
SENDER_EMAIL=noreply@careernavigator.com
SESSION_COOKIE_SECURE=True
WEBHOOK_SECRET=<generate-a-random-secret>
AGENT_POLL_INTERVAL=60
TASK_SCHEDULER_INTERVAL=3600
```

**Security Note:** Never commit `.env` to GitHub. Use Railway's Variables tab for secrets.

### Step 6: Verify Deployment

1. Railway dashboard shows **Deployment Status: Success**
2. Under **Domains**, Railway assigns a public URL like:
   ```
   https://career-navigator-production-xxxx.railway.app
   ```
3. Click the domain link or copy and open in browser
4. You should see the Career Navigator login page

### Step 7: Continuous Deployment (Auto-Deploy on Push)

Railway automatically redeploys when you push to GitHub:

```bash
# Make a change to your code
echo "# Updated" >> README.md
git add README.md
git commit -m "Update readme"
git push origin main
```

Watch the Railway dashboard—deployment will start automatically.

## Troubleshooting

### Build fails or app crashes

1. Check **Build Logs** in Railway dashboard
2. Check **Deployment Logs** for runtime errors
3. Ensure all required dependencies are in `requirements.txt`
4. Verify `Procfile` command is correct

### Database issues (SQLite limits)

On Railway, SQLite works but is not recommended for production. To upgrade:
1. Add PostgreSQL plugin in Railway (free tier available)
2. Update `DATABASE_URL` env var
3. Redeploy

### App stays stuck on "Building"

- Increase build timeout in Railway settings
- Ensure `requirements.txt` doesn't have conflicting versions
- Check Python version compatibility (project uses Python 3.11+)

## Cost & Limits

- **Free Tier:** $5 USD credit/month
- **Typical app usage:** $0–$2/month (dev tier)
- **Overage:** You control spending limits in settings

## Next Steps

1. Once deployed, share the Railway URL with others
2. Add custom domain (optional):
   - Buy domain (Namecheap, Google Domains, etc.)
   - In Railway > Domains > Add Custom Domain
   - Point nameservers to Railway
3. Monitor usage in Railway dashboard (Metrics tab)
4. Scale resources if needed (add Redis, PostgreSQL, more memory)

## Rolling Back / Stopping Deployment

- To pause: Railway > Settings > Pause
- To rollback: Railway > Deployments > Select previous version > Redeploy
- To delete: Railway > Settings > Delete Project

---

**Questions?** Check Railway docs: https://docs.railway.app
