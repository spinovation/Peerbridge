# PeerBridge Deployment Guide

This guide provides step-by-step instructions for deploying the PeerBridge platform to AWS.

## Prerequisites

Before deploying PeerBridge, ensure you have the following:

### Required Tools
- AWS CLI configured with appropriate permissions
- Python 3.11 or later
- Node.js 18+ (for frontend builds)
- Git
- ZIP utility for Lambda packaging

### AWS Permissions
Your AWS user/role needs the following permissions:
- CloudFormation full access
- Lambda full access
- API Gateway full access
- RDS full access
- S3 full access
- IAM role creation and management
- VPC and EC2 networking permissions
- SSM Parameter Store access

## Deployment Steps

### 1. Environment Setup

First, clone the repository and set up your environment:

```bash
git clone https://github.com/spinovation/PeerbridgeSandbox.git
cd PeerbridgeSandbox
```

### 2. Configure Environment Variables

Update the environment configuration file:

```bash
cp config/environment/production.env.example config/environment/production.env
```

Edit `config/environment/production.env` with your actual values:

```bash
# Required: Update these values
DB_PASSWORD=your-secure-database-password
SENDGRID_API_KEY=your-sendgrid-api-key
AWS_ACCOUNT_ID=your-aws-account-id
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key
```

### 3. Deploy Infrastructure

Deploy the AWS infrastructure using CloudFormation:

```bash
# Deploy the complete infrastructure
aws cloudformation create-stack \
  --stack-name peerbridge-production \
  --template-body file://infrastructure/cloudformation/peerbridge-infrastructure-complete.yaml \
  --parameters \
    ParameterKey=Environment,ParameterValue=production \
    ParameterKey=DatabasePassword,ParameterValue=your-secure-password \
    ParameterKey=SendGridApiKey,ParameterValue=your-sendgrid-api-key \
  --capabilities CAPABILITY_NAMED_IAM

# Wait for stack creation to complete
aws cloudformation wait stack-create-complete --stack-name peerbridge-production
```

### 4. Get Infrastructure Outputs

Retrieve the deployed infrastructure details:

```bash
# Get API Gateway URL
API_URL=$(aws cloudformation describe-stacks \
  --stack-name peerbridge-production \
  --query 'Stacks[0].Outputs[?OutputKey==`APIGatewayURL`].OutputValue' \
  --output text)

# Get Database Endpoint
DB_HOST=$(aws cloudformation describe-stacks \
  --stack-name peerbridge-production \
  --query 'Stacks[0].Outputs[?OutputKey==`DatabaseEndpoint`].OutputValue' \
  --output text)

# Get S3 Bucket Names
STATIC_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name peerbridge-production \
  --query 'Stacks[0].Outputs[?OutputKey==`StaticWebsiteBucket`].OutputValue' \
  --output text)

ADMIN_BUCKET=$(aws cloudformation describe-stacks \
  --stack-name peerbridge-production \
  --query 'Stacks[0].Outputs[?OutputKey==`SalesAdminBucket`].OutputValue' \
  --output text)

echo "API URL: $API_URL"
echo "Database Host: $DB_HOST"
echo "Static Bucket: $STATIC_BUCKET"
echo "Admin Bucket: $ADMIN_BUCKET"
```

### 5. Initialize Database

Connect to your RDS instance and initialize the database schema:

```bash
# Install PostgreSQL client if not already installed
sudo apt-get update && sudo apt-get install -y postgresql-client

# Connect to database and run schema
psql -h $DB_HOST -U peerbridge_admin -d peerbridge -f database/schema.sql
```

### 6. Deploy Lambda Function

Package and deploy the Lambda function:

```bash
# Navigate to Lambda function directory
cd backend/lambda-functions

# Install dependencies
pip install -r requirements.txt -t .

# Create deployment package
zip -r lambda-deployment.zip . -x "*.pyc" "__pycache__/*"

# Deploy to Lambda
aws lambda update-function-code \
  --function-name production-peerbridge-api \
  --zip-file fileb://lambda-deployment.zip

# Update environment variables
aws lambda update-function-configuration \
  --function-name production-peerbridge-api \
  --environment Variables="{
    DB_HOST=$DB_HOST,
    DB_NAME=peerbridge,
    DB_USER=peerbridge_admin,
    DB_PASSWORD=your-secure-password,
    DB_PORT=5432,
    SENDGRID_API_KEY=your-sendgrid-api-key,
    ENVIRONMENT=production
  }"

cd ../..
```

### 7. Deploy Frontend Applications

Deploy the Sales Admin dashboard:

```bash
# Update API URL in the frontend
sed -i "s|https://your-api-gateway-url.amazonaws.com/prod|$API_URL|g" frontend/sales-admin/index.html

# Upload to S3
aws s3 cp frontend/sales-admin/index.html s3://$ADMIN_BUCKET/index.html
aws s3 cp frontend/sales-admin/index.html s3://$STATIC_BUCKET/admin/index.html

# Set proper content type and make public
aws s3api put-object-acl --bucket $ADMIN_BUCKET --key index.html --acl public-read
aws s3api put-object-acl --bucket $STATIC_BUCKET --key admin/index.html --acl public-read
```

### 8. Configure Domain and SSL (Optional)

If you have a custom domain:

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --distribution-config file://infrastructure/cloudfront/distribution-config.json

# Update Route 53 records
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch file://infrastructure/route53/record-sets.json
```

### 9. Test Deployment

Test your deployment:

```bash
# Test API endpoints
curl -X GET "$API_URL/api/dashboard-stats"
curl -X GET "$API_URL/api/invitations"

# Test Sales Admin Dashboard
echo "Sales Admin URL: https://$ADMIN_BUCKET.s3-website-us-east-1.amazonaws.com"
```

## Post-Deployment Configuration

### 1. SendGrid Setup

1. Log in to your SendGrid account
2. Create dynamic email templates for:
   - User invitations
   - Welcome emails
   - Password reset emails
3. Update the template IDs in your environment configuration

### 2. Database Monitoring

Set up CloudWatch monitoring for your RDS instance:

```bash
# Enable enhanced monitoring
aws rds modify-db-instance \
  --db-instance-identifier production-peerbridge-db \
  --monitoring-interval 60 \
  --monitoring-role-arn arn:aws:iam::YOUR_ACCOUNT:role/rds-monitoring-role
```

### 3. Lambda Monitoring

Configure CloudWatch alarms for Lambda function:

```bash
# Create error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "PeerBridge-Lambda-Errors" \
  --alarm-description "Lambda function error rate" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=production-peerbridge-api
```

## Troubleshooting

### Common Issues

1. **Lambda Function Timeout**
   - Increase timeout in CloudFormation template
   - Check VPC configuration for database connectivity

2. **Database Connection Issues**
   - Verify security group rules
   - Check VPC subnet configuration
   - Ensure Lambda is in the correct subnets

3. **CORS Errors**
   - Verify API Gateway CORS configuration
   - Check allowed origins in Lambda function

4. **Email Delivery Issues**
   - Verify SendGrid API key
   - Check email template IDs
   - Review SendGrid activity logs

### Debugging Commands

```bash
# Check Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/production-peerbridge"
aws logs get-log-events --log-group-name "/aws/lambda/production-peerbridge-api" --log-stream-name "LATEST"

# Check API Gateway logs
aws logs describe-log-groups --log-group-name-prefix "API-Gateway-Execution-Logs"

# Test database connectivity
psql -h $DB_HOST -U peerbridge_admin -d peerbridge -c "SELECT version();"
```

## Updating the Application

### Lambda Function Updates

```bash
# Update Lambda function code
cd backend/lambda-functions
zip -r lambda-deployment.zip . -x "*.pyc" "__pycache__/*"
aws lambda update-function-code \
  --function-name production-peerbridge-api \
  --zip-file fileb://lambda-deployment.zip
```

### Frontend Updates

```bash
# Update Sales Admin dashboard
aws s3 cp frontend/sales-admin/index.html s3://$ADMIN_BUCKET/index.html
```

### Database Schema Updates

```bash
# Run migration scripts
psql -h $DB_HOST -U peerbridge_admin -d peerbridge -f database/migrations/001_add_new_columns.sql
```

## Security Considerations

1. **Database Security**
   - Use strong passwords
   - Enable encryption at rest
   - Restrict network access via security groups

2. **API Security**
   - Implement rate limiting
   - Use HTTPS only
   - Validate all input data

3. **S3 Security**
   - Use bucket policies to restrict access
   - Enable versioning for important buckets
   - Configure lifecycle policies

## Monitoring and Maintenance

1. **Regular Backups**
   - RDS automated backups are enabled
   - Consider cross-region backup replication

2. **Performance Monitoring**
   - Monitor Lambda execution duration
   - Track API Gateway response times
   - Monitor database performance metrics

3. **Cost Optimization**
   - Review CloudWatch logs retention
   - Monitor S3 storage costs
   - Optimize Lambda memory allocation

## Support

For deployment issues or questions:

1. Check the troubleshooting section above
2. Review CloudWatch logs for error details
3. Submit issues to the GitHub repository
4. Contact the development team

## Cleanup

To remove all resources:

```bash
# Delete CloudFormation stack (this will remove most resources)
aws cloudformation delete-stack --stack-name peerbridge-production

# Manually delete S3 buckets if they contain data
aws s3 rm s3://$STATIC_BUCKET --recursive
aws s3 rm s3://$ADMIN_BUCKET --recursive
aws s3 rm s3://production-peerbridge-user-uploads --recursive

aws s3api delete-bucket --bucket $STATIC_BUCKET
aws s3api delete-bucket --bucket $ADMIN_BUCKET
aws s3api delete-bucket --bucket production-peerbridge-user-uploads
```
