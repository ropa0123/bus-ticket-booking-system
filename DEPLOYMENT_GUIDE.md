# 🚀 Vercel Deployment Guide - Complete Setup

## ✨ What's New

Your bus booking system now has **PostgreSQL database integration** for persistent storage! This means:
- ✅ Bookings persist across deployments
- ✅ Admin panel data doesn't disappear on logout
- ✅ Professional production-ready setup
- ✅ Automatic fallback to in-memory if database unavailable

---

## 📋 Prerequisites

1. [Vercel Account](https://vercel.com/signup) (free)
2. [Git](https://git-scm.com/) installed (optional but recommended)
3. Your project code

---

## 🗄️ Step 1: Set Up Database (Choose One Option)

### Option A: Vercel Postgres (Recommended - Easiest)

1. **Create Vercel Postgres Database**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click **Storage** > **Create Database**
   - Select **Postgres**
   - Choose a database name (e.g., `bus-booking-db`)
   - Select region closest to you
   - Click **Create**

2. **Get Connection String**
   - In your database dashboard, go to **Settings**
   - Copy the `POSTGRES_URL` value
   - Keep this safe - you'll need it!

### Option B: Neon (Free Alternative)

1. Go to [Neon.tech](https://neon.tech)
2. Sign up for free account
3. Create a new project
4. Copy the connection string

### Option C: Supabase (Free Alternative)

1. Go to [Supabase.com](https://supabase.com)
2. Create new project
3. Go to **Settings** > **Database**
4. Copy the connection string (URI format)

---

## 🔧 Step 2: Initialize Database

### Install Dependencies

```bash
cd "D:\My Programs\Bus booking system\web platform"
pip install -r requirements.txt
```

### Create .env File

Create a file named `.env` in your project root:

```env
POSTGRES_URL="your_connection_string_here"
```

Replace `your_connection_string_here` with the connection string from Step 1.

### Run Initialization Script

```bash
python init_db.py
```

You should see:
```
✅ Connected successfully!
✅ Database initialized successfully!
📊 Summary:
   - Routes: 42
   - Bus stops: 7
   - Config items: 4
   - Bookings: 0
```

---

## 🚀 Step 3: Deploy to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Navigate to Your Project**
   ```bash
   cd "D:\My Programs\Bus booking system\web platform"
   ```

4. **Deploy**
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Select your account
   - Link to existing project? **N**
   - Project name? `bus-booking-system` (or your choice)
   - Directory? **.**
   - Override settings? **N**

5. **Add Environment Variable**
   ```bash
   vercel env add POSTGRES_URL
   ```
   - Choose **Production**
   - Paste your database connection string
   - Press Enter

6. **Deploy to Production**
   ```bash
   vercel --prod
   ```

### Method 2: Using Git + Vercel Dashboard

1. **Initialize Git (if not already)**
   ```bash
   git init
   git add .
   git commit -m "Initial commit with database integration"
   ```

2. **Push to GitHub**
   - Create a new repository on [GitHub](https://github.com/new)
   - Follow the instructions to push your code

3. **Import to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/new)
   - Click **Import Project**
   - Select your GitHub repository
   - Click **Import**

4. **Add Environment Variable**
   - In project settings, go to **Settings** > **Environment Variables**
   - Add:
     - Name: `POSTGRES_URL`
     - Value: Your connection string
     - Environment: **Production**
   - Click **Save**

5. **Redeploy**
   - Go to **Deployments**
   - Click on the three dots menu
   - Select **Redeploy**

---

## ✅ Step 4: Verify Deployment

1. **Open Your Deployed App**
   - Vercel will give you a URL like: `https://your-app.vercel.app`
   - Open it in your browser

2. **Test Booking**
   - Click **Book Ticket**
   - Fill in the form
   - Submit booking
   - Note your ticket ID

3. **Test Admin Panel**
   - Click **Admin Panel** tab
   - Login with:
     - Username: `admin`
     - Password: `admin123`
   - Verify you can see the booking you just created
   - Logout and login again
   - **Your bookings should still be there!** ✅

---

## 🔍 Troubleshooting

### Bookings Still Disappearing?

**Check Environment Variables:**
```bash
vercel env ls
```

Make sure `POSTGRES_URL` is listed for Production.

**Check Logs:**
```bash
vercel logs
```

Look for:
- `✅ Database connection established`
- `❌ Database error:` (if there's an issue)

### Database Connection Error

**Verify Connection String Format:**
```
postgresql://username:password@host:5432/database?sslmode=require
```

**Test Connection Locally:**
```bash
python -c "import psycopg2; import os; conn = psycopg2.connect(os.environ['POSTGRES_URL']); print('✅ Connected!'); conn.close()"
```

### Vercel Deployment Fails

**Check vercel.json:**
Make sure it's properly configured (it should already be).

**Check Requirements:**
```bash
pip install -r requirements.txt
```

All dependencies should install without errors.

---

## 🛠️ Local Development

To run locally with database:

```bash
# Set environment variable
export POSTGRES_URL="your_connection_string"

# Or use .env file (already created)

# Run the app
python api/index.py
```

Open http://localhost:5000

---

## 📊 Database Management

### View Database Data

Connect using any PostgreSQL client:
- **pgAdmin** (GUI)
- **DBeaver** (GUI)
- **psql** (CLI)
- **TablePlus** (GUI)

### Backup Database

Using pg_dump:
```bash
pg_dump "your_connection_string" > backup.sql
```

### Reset Database

```bash
python init_db.py
```

This will recreate all tables with default data.

---

## 🔒 Security Notes

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Change admin password** in production:
   - Edit `api/index.py`
   - Update `ADMIN_CREDENTIALS` dictionary
3. **Use environment variables** for all secrets
4. **Enable SSL** for database connections (already configured)

---

## 📝 Files Created

New files for database integration:
- `database.sql` - Database schema with default data
- `db_manager.py` - Database connection and operations
- `init_db.py` - Database initialization script
- `.env.example` - Environment variable template
- `DATABASE_SETUP.md` - Detailed database setup guide
- This deployment guide

Modified files:
- `api/index.py` - Updated to use PostgreSQL
- `requirements.txt` - Added database dependencies

---

## 🎉 Success Checklist

- [ ] Database created (Vercel Postgres, Neon, or Supabase)
- [ ] Database initialized with `init_db.py`
- [ ] Environment variable `POSTGRES_URL` set in Vercel
- [ ] App deployed to Vercel
- [ ] Can create bookings
- [ ] Can view bookings in admin panel
- [ ] Bookings persist after logout/login
- [ ] Bookings persist after redeployment

---

## 🆘 Need Help?

- **Vercel Docs**: https://vercel.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **Neon Docs**: https://neon.tech/docs
- **Supabase Docs**: https://supabase.com/docs

---

## 🚀 Next Steps

1. **Custom Domain**: Add your own domain in Vercel settings
2. **Email Notifications**: Add email service for booking confirmations
3. **Payment Integration**: Add payment gateway (Stripe, PayPal, etc.)
4. **Analytics**: Add Google Analytics or Vercel Analytics
5. **Monitoring**: Set up error tracking (Sentry, etc.)

---

**Congratulations! Your bus booking system is now production-ready with persistent database storage!** 🎉
