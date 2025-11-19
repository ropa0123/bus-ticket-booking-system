# ⚡ Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Prerequisites
- A Vercel account (free) - [Sign up here](https://vercel.com/signup)
- Node.js installed - [Download here](https://nodejs.org/)

---

## 🎯 Fastest Deployment Method

### Step 1: Install Vercel CLI
Open Command Prompt or PowerShell and run:
```bash
npm install -g vercel
```

### Step 2: Navigate to Project
```bash
cd "D:\My Programs\Bus booking system\web platform"
```

### Step 3: Login to Vercel
```bash
vercel login
```
Follow the browser prompt to login.

### Step 4: Deploy
```bash
vercel
```

Answer the prompts:
- **Set up and deploy?** → Press Y
- **Which scope?** → Choose your account
- **Link to existing project?** → Press N
- **Project name?** → Type: `chikukwa-bus`
- **Directory?** → Just press Enter

### Step 5: Production Deploy
```bash
vercel --prod
```

### 🎉 Done!
Your app is live at: `https://chikukwa-bus.vercel.app`

---

## 🧪 Test Your App

Visit your URL and test:

1. **Book a Ticket**
   - Click "Book Ticket"
   - Fill the form
   - Get your ticket ID

2. **Admin Login**
   - Click "Admin Panel" tab
   - Username: `admin`
   - Password: `admin123`
   - View dashboard

3. **View Schedules**
   - Click "View Schedule"
   - See all bus routes

---

## ⚠️ Important: Security

**Before sharing with users**, change admin passwords:

1. Open: `api/index.py`
2. Find line ~17:
   ```python
   ADMIN_CREDENTIALS = {
       "admin": hashlib.sha256("admin123".encode()).hexdigest(),
   ```
3. Change `"admin123"` to your strong password
4. Redeploy: `vercel --prod`

---

## 📚 Need More Help?

- **Full Guide**: See `DEPLOY_GUIDE.md`
- **Documentation**: See `README.md`
- **Support**: support@chikukwabus.com

---

## 🐛 Common Issues

### "npm: command not found"
**Solution**: Install Node.js from [nodejs.org](https://nodejs.org/)

### "vercel: command not found"
**Solution**: Run `npm install -g vercel` first

### Build failed on Vercel
**Solution**: Check Vercel logs in dashboard

---

## 📱 Share Your App

After deployment, share your URL:
- `https://your-project.vercel.app`

Consider:
- Adding a custom domain
- Sharing on social media
- Gathering user feedback

---

**That's it! You're live! 🎉**

*Total time: ~5 minutes*
