#!/usr/bin/env python3
"""
Add customer_id column to the invitations table and populate it
"""
import psycopg2

# Database connection parameters
DB_HOST = "peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com"
DB_NAME = "peerbridge"
DB_USER = "peerbridge_admin"
DB_PASSWORD = "bxWSK7fWIHKDllrc0vVc"
DB_PORT = 5432

def add_customer_id_column():
    """Add customer_id column and populate it"""
    try:
        print(f"🔍 Connecting to database...")
        
        # Connect to database
        conn_string = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} port={DB_PORT}"
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("✅ Connected successfully!")
        
        # Check if customer_id column already exists
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'invitations' AND column_name = 'customer_id'
        """)
        
        column_exists = cursor.fetchone()
        
        if column_exists:
            print("ℹ️  customer_id column already exists")
        else:
            print("📝 Adding customer_id column...")
            
            # Add customer_id column
            cursor.execute("""
                ALTER TABLE invitations 
                ADD COLUMN customer_id VARCHAR(20) UNIQUE
            """)
            
            print("✅ customer_id column added")
        
        # Update existing records with customer_id values
        print("📝 Updating existing records with customer_id values...")
        
        cursor.execute("""
            UPDATE invitations 
            SET customer_id = 'CUST' || LPAD(id::text, 3, '0')
            WHERE customer_id IS NULL
        """)
        
        updated_rows = cursor.rowcount
        print(f"✅ Updated {updated_rows} records with customer_id")
        
        # Commit changes
        conn.commit()
        
        # Show updated table structure
        print(f"\n📋 Updated table structure:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'invitations'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("=" * 60)
        print(f"{'Column Name':<20} {'Data Type':<15} {'Nullable':<10}")
        print("=" * 60)
        for col in columns:
            nullable = "YES" if col[2] == "YES" else "NO"
            print(f"{col[0]:<20} {col[1]:<15} {nullable:<10}")
        
        # Show sample records with customer_id
        print(f"\n📝 Sample records with customer_id:")
        cursor.execute("""
            SELECT id, customer_id, first_name, last_name, email, status
            FROM invitations 
            ORDER BY id
            LIMIT 10
        """)
        
        records = cursor.fetchall()
        print("=" * 80)
        print(f"{'ID':<4} {'Customer ID':<12} {'Name':<20} {'Email':<25} {'Status':<10}")
        print("=" * 80)
        for record in records:
            name = f"{record[2]} {record[3]}"
            print(f"{record[0]:<4} {record[1]:<12} {name:<20} {record[4]:<25} {record[5]:<10}")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Database update completed successfully!")
        print(f"   - customer_id column added")
        print(f"   - {updated_rows} records updated")
        print(f"   - Ready for Lambda function deployment")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Adding customer_id column to invitations table")
    print("=" * 60)
    add_customer_id_column()
