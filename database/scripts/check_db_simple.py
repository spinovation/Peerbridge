#!/usr/bin/env python3
"""
Simple database check - enter password when prompted
"""
import psycopg2

# Database connection parameters
DB_HOST = "peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com"
DB_NAME = "peerbridge"
DB_USER = "peerbridge_admin"
DB_PORT = 5432

# Get password from user
print("🔐 Enter the database password:")
DB_PASSWORD = input().strip()

try:
    print(f"\n🔍 Connecting to database...")
    
    # Connect to database
    conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
    print("✅ Connected successfully!")
    
    # Show table structure
    print(f"\n📋 Invitations table structure:")
    cursor.execute("""
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns 
        WHERE table_name = 'invitations'
        ORDER BY ordinal_position
    """)
    
    columns = cursor.fetchall()
    print("=" * 80)
    print(f"{'Column Name':<20} {'Data Type':<15} {'Nullable':<10} {'Default':<20}")
    print("=" * 80)
    for col in columns:
        nullable = "YES" if col[2] == "YES" else "NO"
        default = str(col[3]) if col[3] else "None"
        print(f"{col[0]:<20} {col[1]:<15} {nullable:<10} {default:<20}")
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM invitations")
    count = cursor.fetchone()[0]
    print(f"\n📊 Total records: {count}")
    
    # Show all records
    print(f"\n📝 All invitation records:")
    cursor.execute("SELECT * FROM invitations ORDER BY created_at DESC")
    records = cursor.fetchall()
    
    print("=" * 120)
    for i, record in enumerate(records, 1):
        print(f"Record {i}:")
        for j, col in enumerate(columns):
            value = record[j] if j < len(record) else "N/A"
            print(f"  {col[0]}: {value}")
        print("-" * 60)
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
