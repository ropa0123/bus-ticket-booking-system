# 🚀 Quick Start Guide

## Problem Solved ✅

**Issue**: Bookings were clearing when admin logged out because data was stored in ephemeral `/tmp/` storage on Vercel.

**Solution**: Integrated **PostgreSQL database** for persistent storage. Now all bookings, routes, and configuration persist forever!

---

## What You Need to Do (3 Simple Steps)

### Step 1: Create a Database (5 minutes)

**Easiest Option - Vercel Postgres:**

1. Go to https://vercel.com/dashboard
2. Click **Storage** > **Create Database** > **Postgres**
3. Name it `bus-booking-db`
4. Click **Create**
5. Copy the **POSTGRES_URL** connection string

**Alternative - Neon (Free):**
- Go to https://neon.tech
- Sign up and create a project
- Copy connection string

### Step 2: Initialize Database (2 minutes)

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with your connection string
echo 'POSTGRES_URL="your_connection_string_here"' > .env

# Initialize database
python init_db.py
```

You'll see:
```
✅ Database initialized successfully!
📊 Summary:
   - Routes: 42
   - Bus stops: 7
   - Bookings: 0
```

### Step 3: Deploy (2 minutes)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Add database URL to production
vercel env add POSTGRES_URL
# (Paste your connection string when prompted, choose "Production")

# Deploy to production
vercel --prod
```

**That's it!** 🎉

---

## Test It Works

1. Open your deployed app URL
2. Book a ticket (note the ticket ID)
3. Go to Admin Panel
4. Login (admin/admin123)
5. See your booking in the dashboard
6. **Logout**
7. **Login again**
8. **Your booking is still there!** ✅

---

## Files You Got

New database files:
- ✅ `database.sql` - Database schema
- ✅ `db_manager.py` - Database operations
- ✅ `init_db.py` - Initialization script
- ✅ `.env.example` - Environment template
- ✅ `DATABASE_SETUP.md` - Detailed setup guide
- ✅ `DEPLOYMENT_GUIDE.md` - Full deployment guide
- ✅ `QUICK_START.md` - This file!

Updated files:
- ✅ `api/index.py` - Now uses PostgreSQL
- ✅ `requirements.txt` - Added database packages

---

## Troubleshooting

### "Database URL not found"
Create `.env` file:
```env
POSTGRES_URL="postgresql://user:pass@host:5432/db?sslmode=require"
```

### "Bookings still disappearing"
Check Vercel environment variables:
```bash
vercel env ls
```

Make sure `POSTGRES_URL` is listed. If not:
```bash
vercel env add POSTGRES_URL
```

### "Can't connect to database"
1. Check connection string format
2. Ensure it ends with `?sslmode=require`
3. Test locally:
   ```bash
   python -c "import psycopg2, os; psycopg2.connect(os.environ['POSTGRES_URL']).close(); print('✅ Connected!')"
   ```

---

## What Changed?

### Before ❌
- Data stored in `/tmp/` (temporary)
- Bookings cleared on logout
- Data lost on redeploy
- Not production-ready

### After ✅
- Data stored in PostgreSQL (permanent)
- Bookings persist forever
- Survives redeployments
- Production-ready!

---

## Need More Help?

- **Full Guide**: Read [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Database Details**: Read [DATABASE_SETUP.md](DATABASE_SETUP.md)
- **Vercel Docs**: https://vercel.com/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

---

## Next Steps (Optional)

1. **Change admin password** (edit `api/index.py`)
2. **Add custom domain** (Vercel dashboard)
3. **Set up monitoring** (Vercel Analytics)
4. **Add email notifications** (SendGrid, Mailgun, etc.)

---

**You're all set!** Your bus booking system now has enterprise-grade persistent storage. 🚀

Questions? Check the detailed guides or test the deployment!
