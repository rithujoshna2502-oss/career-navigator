# 🚀 Deploy Career Navigator to Cloud

Choose one of these options to make your app publicly accessible:

## Option 1: Railway.app (EASIEST & RECOMMENDED) ⭐

Railway is the simplest - no credit card required initially.

### Steps:

1. **Sign up for Railway**
   - Go to https://railway.app
   - Click "Start Project"
   - Sign up with GitHub (or email)

2. **Connect your GitHub repo**
   - If not already: Push your project to GitHub
   - In Railway: Click "Deploy from GitHub"
   - Select your repository
   - Click "Deploy Now"

3. **Railway will automatically:**
   - Detect your Python project
   - Install dependencies from `requirements.txt`
   - Run `gunicorn project.app:app` from `Procfile`
   - Assign a public URL (e.g., `https://careernavigator.up.railway.app`)

4. **Add Environment Variables**
   - In Railway Dashboard → Variables
   - Add your `.env` variables:
     ```
     SECRET_KEY=your-secret-key
     MAIL_PASSWORD=your-gmail-app-password
     MAIL_USERNAME=your-email
     DATABASE_URL=postgresql://... (Railway provides this)
     ```

5. **Access Your App**
   - Click "View deployment" or go to the generated URL
   - Share the URL with anyone to access from any device!

---

## Option 2: Heroku (Traditional but requires credit card)

1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Login: `heroku login`
3. Create app: `heroku create careernavigator`
4. Push code: `git push heroku main`
5. Access at: `https://careernavigator.herokuapp.com`

---

## Option 3: Ngrok (Temporary tunnel - for testing)

1. Install: `pip install ngrok`
2. Start server locally: `python run_server.py`
3. In another terminal: `ngrok http 5000`
4. Share the URL (e.g., `https://abc123-def456.ngrok.io`)
5. ⚠️ Note: URL changes when you restart ngrok

---

## Option 4: Google Cloud / AWS / Azure (Advanced)

For production-grade deployment with auto-scaling and custom domains.

---

## After Deployment

✅ **Share Your Public URL:**
- Anyone can access from mobile, laptop, desktop, tablet
- No need to be on same WiFi
- Works worldwide
- 24/7 availability (cloud servers)

**Example:** 
- Before: Only `http://192.168.1.6:5000` (local network)
- After: `https://careernavigator.railway.app` (worldwide)

---

## Recommended Choice: Railway

**Why Railway?**
- Free tier with credits
- No credit card required initially
- Automatic deployments on git push
- PostgreSQL database included
- Environment variables management built-in
- Custom domain support
- Simple and fast

**Deploy in 5 minutes!**
