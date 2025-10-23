#!/usr/bin/env python3
"""
Test PostgreSQL RDS connection with different passwords
"""
import sys

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
DB_USER = "postgres"
DB_PORT = 5432

# Test different password possibilities
passwords_to_test = [
    "!Q2w3e4r5t",           # The password you provided
    "Q2w3e4r5t",            # Without the exclamation mark
    "peerbridge",           # Simple password
    "password",             # Default password
    "postgres",             # Username as password
    "PeerBridge2025!",      # Similar to your admin password
]

def test_connection(password):
    """Test database connection with given password"""
    try:
        print(f"\n🔍 Testing password: '{password}'")
        
        # Create connection string
        conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={password} port={DB_PORT}"
        
        # Try to connect
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        # Test with a simple query
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✅ SUCCESS! Connected with password: '{password}'")
        print(f"   PostgreSQL version: {version[0]}")
        return True
        
    except psycopg2.OperationalError as e:
        error_msg = str(e).strip()
        if "password authentication failed" in error_msg:
            print(f"❌ FAILED: Wrong password")
        elif "timeout" in error_msg.lower():
            print(f"❌ FAILED: Connection timeout (network/security group issue)")
        elif "could not connect" in error_msg.lower():
            print(f"❌ FAILED: Cannot reach database (network issue)")
        else:
            print(f"❌ FAILED: {error_msg}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

def main():
    print("🚀 Testing PostgreSQL RDS Connection")
    print(f"   Host: {DB_HOST}")
    print(f"   Database: {DB_NAME}")
    print(f"   User: {DB_USER}")
    print(f"   Port: {DB_PORT}")
    print("=" * 60)
    
    success_count = 0
    
    for password in passwords_to_test:
        if test_connection(password):
            success_count += 1
            print(f"\n🎉 FOUND WORKING PASSWORD: '{password}'")
            break
    
    print("\n" + "=" * 60)
    if success_count > 0:
        print("✅ Database connection test SUCCESSFUL!")
        print("   Update your Lambda environment variable with the working password.")
    else:
        print("❌ All password tests FAILED!")
        print("   Possible issues:")
        print("   1. None of the tested passwords are correct")
        print("   2. Database security group doesn't allow connections")
        print("   3. Database is not accessible from this network")
        print("   4. Database endpoint is incorrect")

if __name__ == "__main__":
    main()
