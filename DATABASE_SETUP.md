# Database Setup Guide

Your bus booking system now uses **PostgreSQL** for persistent data storage. This guide will help you set up the database.

## Option 1: Vercel Postgres (Recommended for Vercel Deployment)

### Step 1: Create a Vercel Postgres Database

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Click on **Storage** tab
4. Click **Create Database**
5. Select **Postgres** (powered by Neon)
6. Choose a name for your database
7. Click **Create**

### Step 2: Get Connection String

1. After creation, go to the **Settings** tab of your database
2. Find the **Connection String** section
3. Copy the `POSTGRES_URL` connection string

### Step 3: Add to Vercel Environment Variables

1. In your Vercel project dashboard, go to **Settings** > **Environment Variables**
2. Add a new variable:
   - **Name**: `POSTGRES_URL`
   - **Value**: (paste your connection string)
3. Click **Save**

### Step 4: Initialize Database

Run the initialization script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable temporarily (or use .env file)
export POSTGRES_URL="your_connection_string_here"

# Run initialization script
python init_db.py
```

### Step 5: Deploy

```bash
vercel --prod
```

Your database will now persist data across deployments! ✅

---

## Option 2: Other PostgreSQL Providers

You can use any PostgreSQL provider:

### Popular Options:
- **Neon** (https://neon.tech) - Free tier available
- **Supabase** (https://supabase.com) - Free tier with 500MB
- **Railway** (https://railway.app) - $5/month
- **ElephantSQL** (https://www.elephantsql.com) - Free tier 20MB
- **Amazon RDS** - AWS managed PostgreSQL
- **Google Cloud SQL** - GCP managed PostgreSQL

### Setup Steps:

1. Create a PostgreSQL database with your chosen provider
2. Get the connection string (should look like `postgresql://user:pass@host:5432/db`)
3. Create a `.env` file in your project root:
   ```
   POSTGRES_URL="your_connection_string_here"
   ```
4. Run the initialization script:
   ```bash
   python init_db.py
   ```
5. Add the `POSTGRES_URL` to your Vercel environment variables

---

## Local Development

For local development, you can:

1. **Use a cloud database** (recommended) - Same connection string for local and production
2. **Install PostgreSQL locally**:
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   
   # Ubuntu/Debian
   sudo apt-get install postgresql
   sudo service postgresql start
   
   # Windows
   # Download from https://www.postgresql.org/download/windows/
   ```
   
   Then create a database:
   ```bash
   psql postgres
   CREATE DATABASE bus_booking;
   \q
   ```
   
   Set environment variable:
   ```
   POSTGRES_URL="postgresql://localhost:5432/bus_booking"
   ```

---

## Database Schema

The database includes:

- **bookings** - Stores all ticket bookings
- **routes** - Bus routes with fares and schedules
- **bus_stops** - Bus stop locations by city
- **system_config** - System configuration (seats, contact info, etc.)

All tables are automatically created when you run `init_db.py`.

---

## Fallback Mode

If the database is not available, the application will automatically fall back to **in-memory storage** (data will not persist). You'll see this warning in logs:

```
Warning: Database module not available, using fallback storage
```

To fix this, ensure:
1. `POSTGRES_URL` environment variable is set
2. Database is accessible
3. `psycopg2-binary` is installed

---

## Troubleshooting

### Error: "Database URL not found"
- Make sure `POSTGRES_URL` or `DATABASE_URL` is set in environment variables
- Check that your `.env` file is in the project root
- Verify the connection string format

### Error: "SSL connection required"
- Add `?sslmode=require` to the end of your connection string
- Most cloud databases require SSL

### Error: "Connection timeout"
- Check your database is running
- Verify firewall settings allow connections
- Test connection string with `psql` command

### Error: "Permission denied"
- Verify your database user has CREATE and INSERT permissions
- Check the username and password in connection string

---

## Testing Database Connection

Test your connection:

```python
import psycopg2
import os

conn = psycopg2.connect(os.environ['POSTGRES_URL'])
cursor = conn.cursor()
cursor.execute('SELECT version();')
print(cursor.fetchone())
conn.close()
```

---

## Need Help?

- Vercel Postgres docs: https://vercel.com/docs/storage/vercel-postgres
- PostgreSQL docs: https://www.postgresql.org/docs/
- psycopg2 docs: https://www.psycopg.org/docs/
