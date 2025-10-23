# RDS PostgreSQL Configuration

## Database Details
- **Database Name**: peerbridge
- **Engine**: PostgreSQL 17.4
- **Instance Class**: db.t3.micro
- **Region**: us-east-1
- **Availability Zone**: us-east-1a
- **Storage**: 20 GB General Purpose SSD (gp2)

## Connection Details
- **Endpoint**: peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
- **Port**: 5432
- **Master Username**: peerbridge_admin
- **Database Name**: peerbridge

## Security Groups
- **VPC**: Default VPC
- **Security Group**: Allow PostgreSQL (port 5432) from Lambda functions
- **Publicly Accessible**: No (recommended for security)

## Database Schema

### Invitations Table
```sql
CREATE TABLE invitations (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) UNIQUE,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    status VARCHAR(20) DEFAULT 'sent',
    invitation_code VARCHAR(20) NOT NULL UNIQUE,
    invited_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_on TIMESTAMP,
    expires_on TIMESTAMP,
    user_id INTEGER
);
```

## Environment Variables for Lambda
```
DB_HOST=peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
DB_NAME=peerbridge
DB_USER=peerbridge_admin
DB_PASSWORD=[SECURE_PASSWORD]
DB_PORT=5432
```

## Backup Configuration
- **Automated Backups**: Enabled
- **Backup Retention**: 7 days
- **Backup Window**: 03:00-04:00 UTC
- **Maintenance Window**: Sun 04:00-05:00 UTC

## Monitoring
- **Enhanced Monitoring**: Disabled (to reduce costs)
- **Performance Insights**: Disabled
- **CloudWatch Logs**: Enabled for PostgreSQL logs

## Cost Optimization
- **Instance Type**: db.t3.micro (lowest cost option)
- **Storage**: 20 GB (minimum for production)
- **Multi-AZ**: Disabled (single AZ for cost savings)
