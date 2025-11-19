#!/usr/bin/env python3
"""
Database initialization script for Chikukwa Bus Booking System
Run this script once to initialize your database with the schema and default data
"""

import os
import sys
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def init_database():
    """Initialize the database with schema and default data"""
    
    # Get database URL from environment
    database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ Error: Database URL not found!")
        print("Please set POSTGRES_URL or DATABASE_URL environment variable")
        print("You can also create a .env file with the database URL")
        sys.exit(1)
    
    # Ensure SSL mode is set
    if 'sslmode' not in database_url:
        database_url += '?sslmode=require'
    
    print("🔌 Connecting to database...")
    
    try:
        # Connect to database
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        print("📦 Reading SQL schema file...")
        
        # Read and execute the SQL file
        with open('database.sql', 'r') as f:
            sql_script = f.read()
        
        print("🔧 Creating tables and inserting default data...")
        cursor.execute(sql_script)
        conn.commit()
        
        print("✅ Database initialized successfully!")
        print("\n📊 Summary:")
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM routes")
        routes_count = cursor.fetchone()[0]
        print(f"   - Routes: {routes_count}")
        
        cursor.execute("SELECT COUNT(*) FROM bus_stops")
        stops_count = cursor.fetchone()[0]
        print(f"   - Bus stops: {stops_count}")
        
        cursor.execute("SELECT COUNT(*) FROM system_config")
        config_count = cursor.fetchone()[0]
        print(f"   - Config items: {config_count}")
        
        cursor.execute("SELECT COUNT(*) FROM bookings")
        bookings_count = cursor.fetchone()[0]
        print(f"   - Bookings: {bookings_count}")
        
        print("\n✨ Your database is ready to use!")
        print("\n🚀 Next steps:")
        print("   1. Deploy to Vercel or run locally")
        print("   2. The API will automatically use the database")
        print("   3. Test your booking system!")
        
        cursor.close()
        conn.close()
        
    except FileNotFoundError:
        print("❌ Error: database.sql file not found!")
        print("Make sure you're running this script from the project directory")
        sys.exit(1)
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("  Chikukwa Bus Booking System - Database Initialization")
    print("=" * 60)
    print()
    init_database()
