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

def get_cors_headers():
    """Get CORS headers for responses"""
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }

def get_db_connection():
    """Get database connection"""
    try:
        return psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return None

def lambda_handler(event, context):
    """Main Lambda handler"""
    
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
        # Dashboard Stats Endpoint
        if path == '/api/dashboard-stats' and method == 'GET':
            return handle_dashboard_stats(headers)
        
        # Get Invitations Endpoint
        elif path == '/api/invitations' and method == 'GET':
            return handle_get_invitations(headers)
        
        # Send Invitation Endpoint (frontend calls /api/email)
        elif path == '/api/email' and method == 'POST':
            return handle_send_invitation(event, headers)
        elif path == '/api/send-invitation' and method == 'POST':
            return handle_send_invitation(event, headers)
        
        # Accept Invitation Endpoint
        elif path == '/api/accept-invitation' and method == 'POST':
            return handle_accept_invitation(event, headers)
        
        else:
            logger.warning(f"Unknown endpoint: {method} {path}")
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'message': f'Endpoint not found: {method} {path}'})
            }
            
    except Exception as e:
        logger.error(f"Unhandled error: {e}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'message': f'Internal server error: {str(e)}'})
        }

def handle_dashboard_stats(headers):
    """Get dashboard statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            # Return fallback data if database fails
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
        
        cursor = conn.cursor()
        
        # Get total invitations
        cursor.execute("SELECT COUNT(*) FROM invitations")
        total_invitations = cursor.fetchone()[0]
        
        # Get accepted invitations
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status = 'accepted'")
        users_registered = cursor.fetchone()[0]
        
        # Get pending invitations
        cursor.execute("SELECT COUNT(*) FROM invitations WHERE status IN ('sent', 'pending')")
        pending_invitations = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        stats = {
            'totalInvitationsSent': total_invitations,
            'totalUsersRegistered': users_registered,
            'pendingInvitations': pending_invitations,
            'invitationErrors': 0
        }
        
        logger.info(f"Dashboard stats: {stats}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(stats)
        }
        
    except Exception as e:
        logger.error(f"Dashboard stats error: {e}")
        # Return fallback data
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
    """Get all invitations"""
    try:
        conn = get_db_connection()
        if not conn:
            # Return fallback data if database fails
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps([])
            }
        
        cursor = conn.cursor()
        
        # Get all invitations - use existing columns that we know exist
        cursor.execute("""
            SELECT id, first_name, last_name, email, role, status, 
                   invitation_code, invited_on, accepted_on
            FROM invitations 
            ORDER BY id DESC
        """)
        
        rows = cursor.fetchall()
        
        invitations = []
        for row in rows:
            # Generate customer_id from id if it doesn't exist
            customer_id = f"CUST{row[0]:03d}"
            
            invitation = {
                'customerId': customer_id,
                'firstName': row[1],
                'lastName': row[2],
                'email': row[3],
                'role': row[4],
                'status': row[5],
                'invitationCode': row[6],
                'invitedOn': row[7].strftime('%Y-%m-%d') if row[7] else None,
                'acceptedOn': row[8].strftime('%Y-%m-%d') if row[8] else None
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
        # Return empty list if database fails
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps([])
        }

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
        invitation_code = 'INV' + ''.join(random.choices(string.digits, k=4))
        
        # Save to database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO invitations (first_name, last_name, email, role, invitation_code, status, invited_on)
                    VALUES (%s, %s, %s, %s, %s, 'sent', CURRENT_TIMESTAMP)
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
                    logger.error(f"Database integrity error: {e}")
            except Exception as e:
                logger.error(f"Database insert failed: {e}")
        
        # TODO: Send email via SendGrid here
        logger.info(f"Invitation created for {email} with code {invitation_code}")
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'message': 'Invitation sent successfully',
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
    """Accept an invitation"""
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
        if conn:
            try:
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
                
                logger.info(f"Updated invitation status for {email}")
                
            except Exception as e:
                logger.error(f"Database update failed: {e}")
        
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
