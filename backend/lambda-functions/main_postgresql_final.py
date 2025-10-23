import json
import os
import uuid
import psycopg2
from datetime import datetime
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

def get_db_connection():
    """Get database connection"""
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not set")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

def init_database():
    """Initialize database tables if they don't exist"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Create invitations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invitations (
                id SERIAL PRIMARY KEY,
                customer_id VARCHAR(50) UNIQUE NOT NULL,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                role VARCHAR(50) NOT NULL,
                status VARCHAR(20) DEFAULT 'sent',
                invitation_code VARCHAR(20) UNIQUE NOT NULL,
                invited_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accepted_on TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create index on email for faster lookups
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_invitations_email ON invitations(email)
        """)
        
        # Create index on status for faster filtering
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_invitations_status ON invitations(status)
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def lambda_handler(event, context):
    """Main Lambda handler"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    }
    
    try:
        # Handle preflight requests
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'CORS preflight'})
            }
        
        # Initialize database on first run
        init_database()
        
        # Parse the request
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        logger.info(f"Request: {method} {path}")
        
        # Route requests
        if path == '/api/dashboard-stats' and method == 'GET':
            return handle_dashboard_stats(headers)
        elif path == '/api/invitations' and method == 'GET':
            return handle_get_invitations(headers)
        elif path == '/api/email' and method == 'POST':
            return handle_send_invitation(event, headers)
        elif path.startswith('/api/invitation/accept') and method == 'POST':
            return handle_accept_invitation(event, headers)
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': f'Endpoint not found: {method} {path}'})
            }
            
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Internal server error: {str(e)}'})
        }

def handle_dashboard_stats(headers):
    """Get dashboard statistics from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total invitations sent
        cursor.execute("SELECT COUNT(*) FROM invitations")
        total_sent = cursor.fetchone()[0]
        
        # Get total users registered (accepted invitations)
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status = 'accepted'")
        total_registered = cursor.fetchone()[0]
        
        # Get pending invitations
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status IN ('sent', 'pending')")
        pending = cursor.fetchone()[0]
        
        # Get invitation errors
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status = 'error'")
        errors = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        stats = {
            'totalInvitationsSent': total_sent,
            'totalUsersRegistered': total_registered,
            'pendingInvitations': pending,
            'invitationErrors': errors
        }
        
        logger.info(f"Dashboard stats: {stats}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(stats)
        }
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Failed to get dashboard stats: {str(e)}'})
        }

def handle_get_invitations(headers):
    """Get all invitations from database"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all invitations ordered by invited_on desc
        cursor.execute("""
            SELECT customer_id, first_name, last_name, email, role, status, 
                   invitation_code, invited_on, accepted_on
            FROM invitations 
            ORDER BY invited_on DESC
        """)
        
        rows = cursor.fetchall()
        
        invitations = []
        for row in rows:
            invitation = {
                'customerId': row[0],
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
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Failed to get invitations: {str(e)}'})
        }

def handle_send_invitation(event, headers):
    """Send a new invitation and store in database"""
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        first_name = body.get('firstName')
        last_name = body.get('lastName')
        email = body.get('email')
        role = body.get('role', 'user').lower()
        
        logger.info(f"Sending invitation to: {first_name} {last_name} <{email}> as {role}")
        
        if not all([first_name, last_name, email]):
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'message': 'Missing required fields'})
            }
        
        # Generate unique IDs
        customer_id = f"CUST{str(uuid.uuid4())[:8].upper()}"
        invitation_code = f"INV{str(uuid.uuid4())[:4].upper()}"
        
        # Insert into database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO invitations (customer_id, first_name, last_name, email, role, invitation_code, status)
                VALUES (%s, %s, %s, %s, %s, %s, 'sent')
            """, (customer_id, first_name, last_name, email, role, invitation_code))
            
            conn.commit()
            
        except psycopg2.IntegrityError as e:
            conn.rollback()
            if 'email' in str(e):
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'message': 'Email already exists'})
                }
            else:
                raise e
        
        cursor.close()
        conn.close()
        
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
                'customerId': customer_id,
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
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update invitation status
        cursor.execute("""
            UPDATE invitations 
            SET status = 'accepted', accepted_on = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
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

def send_invitation_email(first_name, last_name, email, role, invitation_code):
    """Send invitation email using SendGrid"""
    try:
        import sendgrid
        from sendgrid.helpers.mail import Mail
        
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        
        # Create email content
        subject = "You're invited to join PeerBridge!"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="text-align: center; margin-bottom: 30px;">
                <h1 style="color: #000; font-size: 32px; font-weight: 900; letter-spacing: 1px; margin: 0;">PEER BRIDGE</h1>
                <p style="color: #666; font-family: 'Ink Free', cursive; font-size: 18px; margin: 5px 0;">Fund Smarter, Build Together</p>
            </div>
            
            <h2 style="color: #333;">Welcome to PeerBridge!</h2>
            
            <p>Hi {first_name},</p>
            
            <p>You've been invited to join <strong>PeerBridge</strong> - Fund Smarter, Build Together.</p>
            
            <p><strong>Your Role:</strong> {role.title()}</p>
            <p><strong>Invitation Code:</strong> {invitation_code}</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="https://peerbridge.ai/register.html?code={invitation_code}&email={email}" 
                   style="background-color: #4F46E5; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold;">
                    Accept Invitation & Register
                </a>
            </div>
            
            <p>If you have any questions, feel free to reach out to our team.</p>
            
            <p>Best regards,<br>The PeerBridge Team</p>
            
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
            <p style="text-align: center; color: #666; font-size: 12px;">
                PeerBridge - Fund Smarter, Build Together
            </p>
        </div>
        """
        
        message = Mail(
            from_email='noreply@peerbridge.ai',
            to_emails=email,
            subject=subject,
            html_content=html_content
        )
        
        response = sg.send(message)
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        raise e
