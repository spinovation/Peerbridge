# S3 Configuration

## Buckets Overview

### 1. Static Website Hosting
- **Bucket Name**: peerbridge-static-site
- **Purpose**: Host public website and static assets
- **Region**: us-east-1
- **Public Access**: Enabled for website hosting
- **Static Website Hosting**: Enabled
- **Index Document**: index.html
- **Error Document**: error.html

### 2. Sales Admin Dashboard
- **Bucket Name**: peerbridge-sales-admin
- **Purpose**: Host sales admin dashboard
- **Region**: us-east-1
- **Public Access**: Restricted (admin only)
- **CloudFront**: Optional for better performance

### 3. User Uploads
- **Bucket Name**: peerbridge-user-uploads
- **Purpose**: Store user-uploaded files (profiles, documents)
- **Region**: us-east-1
- **Public Access**: Private
- **Versioning**: Enabled
- **Encryption**: AES-256

### 4. Application Assets
- **Bucket Name**: peerbridge-app-assets
- **Purpose**: Store application assets, images, documents
- **Region**: us-east-1
- **Public Access**: Public read for assets
- **CDN**: CloudFront distribution recommended

## Bucket Policies

### Static Website Bucket Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::peerbridge-static-site/*"
        }
    ]
}
```

### User Uploads Bucket Policy
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "RestrictToLambdaFunctions",
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::ACCOUNT-ID:role/lambda-execution-role"
            },
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": "arn:aws:s3:::peerbridge-user-uploads/*"
        }
    ]
}
```

## CORS Configuration
```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
        "AllowedOrigins": ["https://peerbridge.ai", "https://www.peerbridge.ai"],
        "ExposeHeaders": []
    }
]
```

## Lifecycle Policies

### User Uploads Lifecycle
- **Transition to IA**: After 30 days
- **Transition to Glacier**: After 90 days
- **Delete**: After 365 days (for temporary files)

## Security Settings
- **Block Public Access**: Enabled for private buckets
- **Server-Side Encryption**: AES-256
- **Access Logging**: Enabled
- **Versioning**: Enabled for critical buckets
- **MFA Delete**: Enabled for production

## Cost Optimization
- **Storage Class**: Standard for frequently accessed files
- **Intelligent Tiering**: Enabled for variable access patterns
- **Lifecycle Rules**: Configured to move old files to cheaper storage
- **CloudFront**: Used to reduce data transfer costs
