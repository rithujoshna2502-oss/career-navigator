# Email Notifications Setup Guide

## 🚀 Quick Setup (Choose One)

### Option 1: SendGrid (Recommended - Free 100 emails/day)

1. **Sign up at https://sendgrid.com** (free account)
2. **Get API Key:**
   - Go to Settings → API Keys
   - Create new API Key (Full Access)
   - Copy the key
3. **Create `.env` file in project root:**
   ```bash
   MAIL_SERVER=smtp.sendgrid.net
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=apikey
   MAIL_PASSWORD=SG.your-api-key-here
   SENDER_EMAIL=noreply@yourdomain.com
   ```
4. **Test it:**
   - Restart the app
   - Login to dashboard
   - Click "Send Test Email" button
   - Check your email!

---

### Option 2: Gmail SMTP (Free, needs app password)

1. **Enable 2-factor authentication on your Google account**
2. **Create App Password:**
   - Go to https://myaccount.google.com/apppasswords
   - Select Mail + Windows Computer
   - Copy the generated password
3. **Create `.env` file:**
   ```bash
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password-here
   SENDER_EMAIL=your-email@gmail.com
   ```
4. **Test it** (same as above)

---

### Option 3: Development Mode (No Email Provider)

If you don't want to set up an email service yet:
- Leave `MAIL_PASSWORD` empty
- Emails will be logged to console (you'll see them in terminal)
- Perfect for local testing!

---

## 🧪 Testing Email Service

### Local Testing (Console Output)
```bash
# 1. Start the app
python project/app.py

# 2. Register and login to http://127.0.0.1:5000
# 3. Go to Dashboard → Step 3 (Track Progress)
# 4. Click "Send Test Email"
# 5. Check your terminal for console output
```

### Production Testing (Cloud)
- Deploy to Railway (see DEPLOYMENT.md)
- Set env vars in Railway dashboard
- Test email endpoint via API

---

## 📧 Automated Email Triggers (When Enabled)

Once configured, emails will be sent automatically for:

1. **Daily Reminders** (optional - implement scheduler)
   - Time: 8:00 AM user's timezone
   - Content: Today's task + motivation

2. **Tech Update Alerts** (when new tech detected)
   - Triggered: When `/api/check-tech-updates` finds new tech
   - Content: List of new technologies + link to plan

3. **Plan Update Confirmation** (when plan updated)
   - Triggered: After user accepts tech update
   - Content: Summary of changes + new version number

---

## 🔧 Troubleshooting

### Email not sending?
1. Check `.env` file exists and has correct values
2. Verify API key is valid (try in SendGrid dashboard)
3. Check terminal logs for error messages
4. Make sure `MAIL_PASSWORD` is not empty

### App crashes on startup?
- Ensure `flask-mail` is installed: `pip install flask-mail`
- Check `.env` syntax (no spaces around `=`)

### Test email button doesn't appear?
- You must be logged in
- Go to Dashboard (Step 3)
- Scroll down to Tech Update section

---

## 📚 Next Steps

1. Choose email provider (SendGrid recommended)
2. Get API credentials
3. Create `.env` file with credentials
4. Restart app
5. Test it!

Questions? Check the logs in your terminal for detailed error messages.
