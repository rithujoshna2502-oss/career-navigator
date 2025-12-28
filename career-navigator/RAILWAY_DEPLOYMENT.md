# 🌐 QUICK START: Deploy to Railway (5 Minutes)

## Step 1: Push to GitHub

```bash
cd c:\Users\rithu\myprojectenv
git init
git add .
git commit -m "Career Navigator - Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/career-navigator.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

---

## Step 2: Deploy on Railway

1. Go to **https://railway.app**
2. Click **"Start a New Project"** → **"Deploy from GitHub"**
3. Authorize Railway to access your GitHub
4. Select your **career-navigator** repository
5. Click **"Deploy Now"** ✅

Railway will automatically:
- Detect Python project
- Install dependencies
- Start your app
- Assign a public URL

---

## Step 3: Configure Environment Variables

In Railway Dashboard:

1. Click your project
2. Go to **"Variables"** tab
3. Add these variables:

```
SECRET_KEY=your-random-secret-key-123456
MAIL_PASSWORD=your-gmail-app-password
MAIL_USERNAME=your-email@gmail.com
ENVIRONMENT=production
```

---

## Step 4: Access Your App

✅ Railway assigns a public URL automatically!

Example: `https://careernavigator-production.up.railway.app`

**Share this link with anyone** - they can access from:
- 📱 Mobile phones
- 💻 Laptops
- 🖥️ Desktops
- ⌚ Any device with a browser

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| App crashes on deployment | Check Railway logs: click "Logs" tab |
| Database errors | Railway auto-creates PostgreSQL - no extra setup needed |
| Emails not sending | Add `MAIL_PASSWORD` in Variables |
| 404 errors | Clear browser cache, try incognito mode |

---

## Next: Buy a Custom Domain (Optional)

In Railway:
1. Go to **"Domains"**
2. Click **"Add Domain"**
3. Enter your domain (e.g., `careernavigator.com`)
4. Update your domain's DNS settings
5. Your app is now at `https://careernavigator.com`

---

## What's Next?

After deployment:
- ✅ Anyone can access from any device worldwide
- ✅ 24/7 uptime (cloud servers)
- ✅ Automatic HTTPS (SSL certificate)
- ✅ Free tier with credits
- ✅ Easy to scale if needed

**Your Career Navigator is now live!** 🚀
