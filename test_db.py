#!/usr/bin/env python3
"""
Quick database connection test script
Run this to verify your database setup is working
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection and show some info"""
    
    print("=" * 60)
    print("  Database Connection Test")
    print("=" * 60)
    print()
    
    # Check for database URL
    database_url = os.environ.get('POSTGRES_URL') or os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ No database URL found!")
        print()
        print("Please set POSTGRES_URL environment variable:")
        print("  1. Create a .env file with:")
        print('     POSTGRES_URL="your_connection_string"')
        print("  2. Or set environment variable:")
        print("     export POSTGRES_URL='your_connection_string'")
        sys.exit(1)
    
    print(f"✅ Database URL found")
    print(f"   Host: {database_url.split('@')[1].split(':')[0] if '@' in database_url else 'Unknown'}")
    print()
    
    # Try to import psycopg2
    try:
        import psycopg2
        print("✅ psycopg2 installed")
    except ImportError:
        print("❌ psycopg2 not installed")
        print()
        print("Install it with:")
        print("  pip install psycopg2-binary")
        sys.exit(1)
    
    # Ensure SSL mode
    if 'sslmode' not in database_url:
        database_url += '?sslmode=require'
    
    # Try to connect
    print()
    print("🔌 Attempting connection...")
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        print()
        
        # Get PostgreSQL version
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f"📊 PostgreSQL version:")
        print(f"   {version.split(',')[0]}")
        print()
        
        # Check if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"✅ Found {len(tables)} tables:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                print(f"   - {table[0]}: {count} rows")
        else:
            print("⚠️  No tables found - run init_db.py to create them")
        
        print()
        print("=" * 60)
        print("✅ Database is ready to use!")
        print("=" * 60)
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Connection failed!")
        print(f"   Error: {e}")
        print()
        print("Common issues:")
        print("  1. Check connection string format")
        print("  2. Ensure database allows connections from your IP")
        print("  3. Verify credentials are correct")
        print("  4. Check if database is running")
        sys.exit(1)
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_database_connection()
