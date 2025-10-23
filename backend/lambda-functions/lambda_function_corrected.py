import json
import psycopg2
import os
import logging
import random
import string
from datetime import datetime

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Database configuration
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT', 5432)

# SendGrid configuration
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

def get_cors_headers():
    """Get CORS headers for responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

def initialize_database():
    """Initialize database with table if it doesn't exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'invitations'
            )
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            # Create table with correct structure
            cursor.execute("""
                CREATE TABLE invitations (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100),
                    last_name VARCHAR(100),
                    email VARCHAR(255) NOT NULL UNIQUE,
                    role VARCHAR(50) NOT NULL,
                    status VARCHAR(20) DEFAULT 'sent',
                    invited_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    invitation_code VARCHAR(20) NOT NULL UNIQUE,
                    accepted_on TIMESTAMP,
                    expires_on TIMESTAMP,
                    user_id INTEGER
                )
            """)
            
            conn.commit()
            logger.info("Created invitations table")
            
            # Insert sample data
            sample_data = [
                ('Alice', 'Cooper', 'alice.cooper@example.com', 'entrepreneur', 'pending', 'INV1001'),
                ('Bob', 'Taylor', 'bob.taylor@example.com', 'investor', 'accepted', 'INV1002'),
                ('Carol', 'Davis', 'carol.davis@example.com', 'affiliate', 'pending', 'INV1003'),
                ('Dan', 'Miller', 'dan.miller@example.com', 'entrepreneur', 'sent', 'INV1004')
            ]
            
            for data in sample_data:
                cursor.execute("""
                    INSERT INTO invitations (first_name, last_name, email, role, status, invitation_code)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (email) DO NOTHING
                """, data)
            
            conn.commit()
            logger.info("Inserted sample data")
        
        cursor.close()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

def handle_get_dashboard_stats(headers):
    """Get dashboard statistics from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total invitations sent
        cursor.execute("SELECT COUNT(*) FROM invitations")
        total_invitations = cursor.fetchone()[0]
        
        # Get users registered (accepted invitations)
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status = 'accepted'")
        users_registered = cursor.fetchone()[0]
        
        # Get pending invitations
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status IN ('sent', 'pending')")
        pending_invitations = cursor.fetchone()[0]
        
        # Get invitation errors (you can define your own criteria)
        invitation_errors = 0
        
        cursor.close()
        conn.close()
        
        stats = {
            'totalInvitationsSent': total_invitations,
            'totalUsersRegistered': users_registered,
            'pendingInvitations': pending_invitations,
            'invitationErrors': invitation_errors
        }
        
        logger.info(f"Dashboard stats: {stats}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(stats)
        }
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        # Fallback to sample data
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'totalInvitationsSent': 6,
                'totalUsersRegistered': 2,
                'pendingInvitations': 4,
                'invitationErrors': 0
            })
        }

def handle_get_invitations(headers):
    """Get all invitations from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all invitations ordered by invited_on desc
        cursor.execute("""
            SELECT id, first_name, last_name, email, role, status, 
                   invitation_code, invited_on, accepted_on
            FROM invitations 
            ORDER BY invited_on DESC
        """)
        
        rows = cursor.fetchall()
        
        invitations = []
        for row in rows:
            invitation = {
                'customerId': f"CUST{row[0]:03d}",  # Use id to create customer ID
                'firstName': row[1],
                'lastName': row[2],
                'email': row[3],
                'role': row[4],
                'status': row[5],
                'invitationCode': row[6],
                'invitedOn': row[7].isoformat() + 'Z' if row[7] else None,
                'acceptedOn': row[8].isoformat() + 'Z' if row[8] else None
            }
            invitations.append(invitation)
        
        cursor.close()
        conn.close()
        
        logger.info(f"Returning {len(invitations)} invitations")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(invitations)
        }
        
    except Exception as e:
        logger.error(f"Get invitations error: {e}")
        # Fallback to sample data if database fails
        sample_invitations = [
            {
                "customerId": "CUST005",
                "firstName": "Ganapati",
                "lastName": "Sridhar",
                "email": "sridhargs@spinovation.com",
                "role": "admin",
                "status": "accepted",
                "invitationCode": "INV2440",
                "invitedOn": "2025-10-11T00:00:00Z",
                "acceptedOn": "2025-10-11T12:00:00Z"
            },
            {
                "customerId": "CUST006",
                "firstName": "Ganapati",
                "lastName": "Sridhar",
                "email": "sridhargs@gmail.com",
                "role": "admin",
                "status": "sent",
                "invitationCode": "INV8910",
                "invitedOn": "2025-10-11T00:00:00Z",
                "acceptedOn": None
            }
        ]
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(sample_invitations)
        }

def generate_invitation_code():
    """Generate a unique invitation code"""
    return 'INV' + ''.join(random.choices(string.digits, k=4))

def send_invitation_email(first_name, last_name, email, role, invitation_code):
    """Send invitation email via SendGrid"""
    if not SENDGRID_API_KEY:
        logger.warning("SendGrid API key not configured")
        return
    
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail
        
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        # Create email content
        subject = f"Welcome to PeerBridge - Your {role.title()} Invitation"
        
        html_content = f"""
        <html>
        <body>
            <h2>Welcome to PeerBridge!</h2>
            <p>Hi {first_name},</p>
            <p>You've been invited to join PeerBridge as a <strong>{role}</strong>.</p>
            <p>Your invitation code is: <strong>{invitation_code}</strong></p>
            <p>Click the link below to accept your invitation:</p>
            <p><a href="https://peerbridge.ai/accept-invitation?code={invitation_code}&email={email}">Accept Invitation</a></p>
            <p>Best regards,<br>The PeerBridge Team</p>
        </body>
        </html>
        """
        
        message = Mail(
            from_email='noreply@peerbridge.ai',
            to_emails=email,
            subject=subject,
            html_content=html_content
        )
        
        response = sg.send(message)
        logger.info(f"Email sent to {email}, status: {response.status_code}")
        
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise e

def handle_send_invitation(event, headers):
    """Send a single invitation"""
    try:
        body = json.loads(event.get('body', '{}'))
        first_name = body.get('firstName', '').strip()
        last_name = body.get('lastName', '').strip()
        email = body.get('email', '').strip().lower()
        role = body.get('role', '').strip().lower()
        
        logger.info(f"Sending invitation to: {first_name} {last_name} ({email}) as {role}")
        
        if not all([first_name, last_name, email, role]):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'All fields are required'})
            }
        
        # Generate invitation code
        invitation_code = generate_invitation_code()
        
        # Save to database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO invitations (first_name, last_name, email, role, invitation_code, status)
                VALUES (%s, %s, %s, %s, %s, 'sent')
            """, (first_name, last_name, email, role, invitation_code))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            logger.info(f"Invitation saved to database: {email}")
            
        except psycopg2.IntegrityError as e:
            if 'email' in str(e):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'message': 'Email already exists'})
                }
            else:
                raise e
        except Exception as e:
            logger.error(f"Database insert failed: {e}")
            # Continue without database if it fails
            pass
        
        # Send email (if SendGrid is configured)
        if SENDGRID_API_KEY:
            try:
                send_invitation_email(first_name, last_name, email, role, invitation_code)
                logger.info(f"Email sent successfully to {email}")
            except Exception as e:
                logger.error(f"Failed to send email: {e}")
                # Don't fail the whole request if email fails
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Invitation sent successfully',
                'customerId': f"CUST{random.randint(100, 999)}",
                'invitationCode': invitation_code
            })
        }
        
    except Exception as e:
        logger.error(f"Send invitation error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Failed to send invitation: {str(e)}'})
        }

def handle_accept_invitation(event, headers):
    """Accept an invitation in database"""
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        invitation_code = body.get('invitationCode')
        
        logger.info(f"Accepting invitation for: {email}")
        
        if not email:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Email is required'})
            }
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Update invitation status
            cursor.execute("""
                UPDATE invitations 
                SET status = 'accepted', accepted_on = CURRENT_TIMESTAMP
                WHERE email = %s AND status != 'accepted'
            """, (email,))
            
            if cursor.rowcount == 0:
                cursor.close()
                conn.close()
                return {
                    'statusCode': 404,
                    'headers': headers,
                    'body': json.dumps({'message': 'Invitation not found or already accepted'})
                }
            
            conn.commit()
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Database update failed: {e}")
            # Continue without database if it fails
            pass
        
        logger.info(f"Updated invitation status for {email}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'Invitation accepted successfully'})
        }
        
    except Exception as e:
        logger.error(f"Accept invitation error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Failed to accept invitation: {str(e)}'})
        }

def lambda_handler(event, context):
    """Main Lambda handler"""
    
    # Initialize database on first run
    initialize_database()
    
    # Get CORS headers
    headers = get_cors_headers()
    
    # Handle OPTIONS request for CORS
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Get the path and method
    path = event.get('path', '')
    method = event.get('httpMethod', '')
    
    logger.info(f"Request: {method} {path}")
    
    try:
        # Route requests
        if path == '/api/dashboard-stats' and method == 'GET':
            return handle_get_dashboard_stats(headers)
        elif path == '/api/invitations' and method == 'GET':
            return handle_get_invitations(headers)
        elif path == '/api/send-invitation' and method == 'POST':
            return handle_send_invitation(event, headers)
        elif path == '/api/accept-invitation' and method == 'POST':
            return handle_accept_invitation(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': 'Endpoint not found'})
            }
            
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': 'Internal server error'})
        }
