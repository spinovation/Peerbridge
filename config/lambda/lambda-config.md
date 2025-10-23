# Lambda Functions Configuration

## Function Overview

### 1. PeerBridge Backend API
- **Function Name**: peer-bridge-backend-v2-PeerBridgeBackendFunctionV2
- **Runtime**: Python 3.11
- **Handler**: lambda_function.lambda_handler
- **Memory**: 128 MB
- **Timeout**: 30 seconds
- **Region**: us-east-1

### API Endpoints
- `GET /api/dashboard-stats` - Dashboard statistics
- `GET /api/invitations` - List all invitations
- `POST /api/email` - Send invitation email
- `POST /api/send-invitation` - Alternative invitation endpoint
- `POST /api/accept-invitation` - Accept invitation
- `GET /api/users` - List users
- `PUT /api/users/{userId}` - Update user
- `DELETE /api/users/{userId}` - Delete user
- `POST /api/users/{userId}/reset-password` - Reset password

## Environment Variables

### Database Configuration
```
DB_HOST=peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
DB_NAME=peerbridge
DB_USER=peerbridge_admin
DB_PASSWORD=[SECURE_PASSWORD]
DB_PORT=5432
```

### Email Configuration
```
SENDGRID_API_KEY=[SENDGRID_API_KEY]
FROM_EMAIL=noreply@peerbridge.ai
```

### Application Configuration
```
ENVIRONMENT=production
DEBUG=false
CORS_ORIGIN=https://peerbridge.ai
```

## IAM Role Permissions

### Lambda Execution Role
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "rds:DescribeDBInstances",
                "rds:Connect"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::peerbridge-user-uploads/*",
                "arn:aws:s3:::peerbridge-app-assets/*"
            ]
        }
    ]
}
```

## VPC Configuration
- **VPC**: Default VPC
- **Subnets**: Private subnets for database access
- **Security Groups**: Allow HTTPS outbound, PostgreSQL to RDS

## Monitoring & Logging
- **CloudWatch Logs**: Enabled
- **Log Retention**: 14 days
- **X-Ray Tracing**: Disabled (to reduce costs)
- **Dead Letter Queue**: Configured for failed invocations

## Deployment Package
- **Size**: ~4.2 MB (includes psycopg2-binary)
- **Dependencies**: 
  - psycopg2-binary (PostgreSQL driver)
  - boto3 (AWS SDK)
  - json, os, datetime (built-in)

## Performance Optimization
- **Memory**: 128 MB (sufficient for current workload)
- **Timeout**: 30 seconds (database operations)
- **Concurrent Executions**: 10 (to control costs)
- **Reserved Concurrency**: Not configured

## Error Handling
- **Retry Configuration**: 2 retries for failed invocations
- **Dead Letter Queue**: SQS queue for failed messages
- **Error Notifications**: CloudWatch alarms for high error rates

## Security
- **Environment Variables**: Encrypted at rest
- **VPC**: Lambda functions in private subnets
- **IAM**: Least privilege access
- **API Gateway**: CORS configured for specific origins
