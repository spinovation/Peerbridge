#!/usr/bin/env python3
"""
Check what's actually in the PostgreSQL database
"""
import sys
import os

# Try to import psycopg2
try:
    import psycopg2
    print("✅ psycopg2 is available")
except ImportError:
    print("❌ psycopg2 not available, installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
    import psycopg2
    print("✅ psycopg2 installed and imported")

# Database connection parameters
DB_HOST = "peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com"
DB_NAME = "peerbridge"
DB_USER = "peerbridge_admin"
DB_PASSWORD = "!Q2w3e4r5t"
DB_PORT = 5432

def check_database():
    """Check what's in the database"""
    try:
        print(f"\n🔍 Connecting to database...")
        print(f"   Host: {DB_HOST}")
        print(f"   Database: {DB_NAME}")
        print(f"   User: {DB_USER}")
        
        # Create connection string
        conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
        
        # Connect to database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        
        # Check if invitations table exists
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'invitations'
        """)
        
        table_exists = cursor.fetchone()
        if table_exists:
            print("✅ Invitations table exists")
        else:
            print("❌ Invitations table does not exist")
            cursor.close()
            conn.close()
            return
        
        # Get table structure
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'invitations'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print(f"\n📋 Table structure ({len(columns)} columns):")
        for col in columns:
            print(f"   {col[0]} ({col[1]}) - {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        # Count total records
        cursor.execute("SELECT COUNT(*) FROM invitations")
        total_count = cursor.fetchone()[0]
        print(f"\n📊 Total invitations in database: {total_count}")
        
        # Get all records
        cursor.execute("""
            SELECT customer_id, first_name, last_name, email, role, status, 
                   invitation_code, invited_on, accepted_on, created_at, updated_at
            FROM invitations 
            ORDER BY created_at DESC
        """)
        
        records = cursor.fetchall()
        
        print(f"\n📝 All invitation records:")
        print("=" * 120)
        print(f"{'ID':<8} {'Name':<20} {'Email':<30} {'Role':<12} {'Status':<10} {'Code':<8} {'Invited On':<20}")
        print("=" * 120)
        
        for record in records:
            customer_id = record[0] or "N/A"
            name = f"{record[1] or ''} {record[2] or ''}".strip() or "N/A"
            email = record[3] or "N/A"
            role = record[4] or "N/A"
            status = record[5] or "N/A"
            code = record[6] or "N/A"
            invited_on = record[7].strftime("%Y-%m-%d %H:%M") if record[7] else "N/A"
            
            print(f"{customer_id:<8} {name:<20} {email:<30} {role:<12} {status:<10} {code:<8} {invited_on:<20}")
        
        # Check for duplicates
        cursor.execute("""
            SELECT email, COUNT(*) as count
            FROM invitations 
            GROUP BY email 
            HAVING COUNT(*) > 1
        """)
        
        duplicates = cursor.fetchall()
        if duplicates:
            print(f"\n⚠️  Duplicate emails found:")
            for dup in duplicates:
                print(f"   {dup[0]}: {dup[1]} records")
        else:
            print(f"\n✅ No duplicate emails found")
        
        # Check status distribution
        cursor.execute("""
            SELECT status, COUNT(*) as count
            FROM invitations 
            GROUP BY status
        """)
        
        status_counts = cursor.fetchall()
        print(f"\n📈 Status distribution:")
        for status in status_counts:
            print(f"   {status[0]}: {status[1]} records")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Database check completed successfully!")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Database connection failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def check_sendgrid_config():
    """Check SendGrid configuration"""
    print(f"\n📧 SendGrid Configuration Check:")
    print("=" * 50)
    
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if sendgrid_key:
        print(f"✅ SENDGRID_API_KEY is set (length: {len(sendgrid_key)})")
        if sendgrid_key.startswith('SG.'):
            print("✅ API key format looks correct")
        else:
            print("⚠️  API key doesn't start with 'SG.' - might be invalid")
    else:
        print("❌ SENDGRID_API_KEY not found in environment")
    
    # Test SendGrid API key if available
    if sendgrid_key and sendgrid_key.startswith('SG.'):
        try:
            import requests
            
            headers = {
                'Authorization': f'Bearer {sendgrid_key}',
                'Content-Type': 'application/json'
            }
            
            # Test API key with a simple API call
            response = requests.get('https://api.sendgrid.com/v3/user/account', headers=headers)
            
            if response.status_code == 200:
                print("✅ SendGrid API key is valid and working")
                account_info = response.json()
                print(f"   Account: {account_info.get('email', 'N/A')}")
            else:
                print(f"❌ SendGrid API key test failed: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"⚠️  Could not test SendGrid API: {e}")

if __name__ == "__main__":
    print("🚀 PeerBridge Database & SendGrid Check")
    print("=" * 60)
    
    check_database()
    check_sendgrid_config()
    
    print(f"\n" + "=" * 60)
    print("🏁 Check completed!")
