# PeerBridge.ai - Professional Networking Platform

[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![AWS](https://img.shields.io/badge/AWS-Lambda%20%7C%20RDS%20%7C%20S3-orange.svg)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/postgresql-17.4-blue.svg)](https://postgresql.org)

PeerBridge.ai is an invitation-only professional networking platform that connects entrepreneurs, investors, and affiliates to facilitate smarter funding and collaborative business building.

## 🚀 Quick Start

### Prerequisites

- AWS CLI configured with appropriate permissions
- Python 3.11 or later
- PostgreSQL client tools
- Git

### Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/spinovation/PeerbridgeSandbox.git
   cd PeerbridgeSandbox
   ```

2. **Configure environment**
   ```bash
   cp config/environment/production.env config/environment/production.env.backup
   # Edit production.env with your actual values
   ```

3. **Deploy infrastructure**
   ```bash
   aws cloudformation create-stack \
     --stack-name peerbridge-production \
     --template-body file://infrastructure/cloudformation/peerbridge-infrastructure-complete.yaml \
     --parameters \
       ParameterKey=DatabasePassword,ParameterValue=your-secure-password \
       ParameterKey=SendGridApiKey,ParameterValue=your-sendgrid-api-key \
     --capabilities CAPABILITY_NAMED_IAM
   ```

4. **Initialize database**
   ```bash
   psql -h your-db-host -U peerbridge_admin -d peerbridge -f database/schema.sql
   ```

5. **Deploy Lambda function**
   ```bash
   cd backend/lambda-functions
   pip install -r requirements.txt -t .
   zip -r lambda-deployment.zip .
   aws lambda update-function-code \
     --function-name production-peerbridge-api \
     --zip-file fileb://lambda-deployment.zip
   ```

For detailed deployment instructions, see [DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md).

## 🏗️ Architecture

PeerBridge is built on a modern serverless architecture using AWS services for scalability, reliability, and cost-effectiveness:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   API Gateway    │    │   Lambda        │
│   (S3 + CF)     │◄──►│   (REST API)     │◄──►│   (Python 3.11) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Email         │    │   File Storage   │    │   Database      │
│   (SendGrid)    │    │   (S3 Buckets)   │    │   (RDS PostgreSQL)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Components

**Frontend Applications** include the public website, sales admin dashboard, and user portal, all hosted on S3 with CloudFront distribution.

**Backend API** is powered by AWS Lambda functions with Python 3.11 runtime, providing RESTful endpoints for all platform operations.

**Database Layer** uses Amazon RDS PostgreSQL for reliable data persistence with automated backups and monitoring.

**Email Services** integrate with SendGrid for transactional emails, notifications, and marketing communications.

**File Storage** utilizes S3 buckets for static assets, user uploads, and document management with appropriate security policies.

## 📁 Project Structure

```
PeerbridgeSandbox/
├── frontend/                    # Frontend applications
│   ├── sales-admin/            # Sales admin dashboard
│   ├── public-site/            # Public website
│   └── user-portal/            # User dashboard
├── backend/                     # Backend services
│   ├── lambda-functions/       # AWS Lambda functions
│   └── api-docs/              # API documentation
├── database/                    # Database files
│   ├── schema.sql             # Database schema
│   ├── migrations/            # Schema migrations
│   └── scripts/               # Utility scripts
├── infrastructure/              # Infrastructure as Code
│   ├── cloudformation/        # CloudFormation templates
│   └── terraform/             # Terraform configurations (future)
├── config/                      # Configuration files
│   ├── environment/           # Environment variables
│   ├── database/             # Database configurations
│   ├── lambda/               # Lambda configurations
│   └── s3/                   # S3 bucket policies
├── docs/                        # Documentation
│   ├── deployment/           # Deployment guides
│   └── api/                  # API documentation
└── assets/                      # Project assets
    ├── images/               # Project images
    └── screenshots/          # Development screenshots
```

## 🎯 Current Status

### ✅ Completed Features

**Infrastructure Foundation** includes AWS RDS PostgreSQL database, Lambda functions, API Gateway, and S3 buckets properly configured and deployed.

**Sales Admin Dashboard** provides invitation management, user statistics, and administrative controls with real-time database integration.

**Database Schema** supports user invitations, customer management, and role-based access with proper indexing and relationships.

**Email Integration** enables automated invitation emails, user notifications, and administrative communications through SendGrid.

**Authentication System** includes user registration, login, and session management with secure token handling.

### 🚧 In Progress

**Database Integration** requires final debugging of dashboard refresh functionality and email delivery confirmation.

**User Interface Enhancement** involves improving the admin dashboard responsiveness and adding better error handling.

**Infrastructure Cleanup** includes removing duplicate resources and optimizing AWS costs.

### 📋 Planned Features

**User Landing Pages** will provide personalized dashboards for entrepreneurs, investors, and affiliates with role-specific functionality.

**Project Management** will enable entrepreneurs to create, edit, and showcase their projects with rich media support.

**Investor Dashboard** will offer investment tracking, due diligence tools, and portfolio management capabilities.

**Matching Algorithm** will intelligently connect entrepreneurs with suitable investors based on industry, stage, and preferences.

**Payment Integration** will handle subscription management, transaction processing, and commission distribution.

**Mobile Applications** will extend platform access through native iOS and Android applications.

## 🛠️ Technology Stack

### Backend
- **Runtime**: Python 3.11
- **Database**: PostgreSQL 17.4
- **API**: RESTful API with AWS Lambda + API Gateway
- **Email**: SendGrid for transactional emails
- **Authentication**: JWT-based authentication

### Frontend
- **Technologies**: HTML5, CSS3, JavaScript ES6+
- **Styling**: CSS Grid, Flexbox, responsive design
- **Icons**: Font Awesome 6.0
- **Hosting**: S3 static website hosting

### Infrastructure
- **Cloud Provider**: Amazon Web Services (AWS)
- **Compute**: AWS Lambda (serverless)
- **Database**: Amazon RDS PostgreSQL
- **Storage**: Amazon S3
- **API**: Amazon API Gateway
- **Monitoring**: CloudWatch Logs and Metrics
- **IaC**: CloudFormation templates

### Development Tools
- **Version Control**: Git
- **CI/CD**: AWS CLI deployment scripts
- **Package Management**: pip (Python), npm (Node.js)
- **Database Tools**: psql, pgAdmin

## 🔧 Configuration

### Environment Variables

Key environment variables that need to be configured:

```bash
# Database Configuration
DB_HOST=peer-bridge-production-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
DB_NAME=peerbridge
DB_USER=peerbridge_admin
DB_PASSWORD=your-secure-password
DB_PORT=5432

# Email Configuration
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@peerbridge.ai

# AWS Configuration
AWS_REGION=us-east-1
API_BASE_URL=https://your-api-gateway-url.amazonaws.com/prod

# Security
JWT_SECRET_KEY=your-jwt-secret-key
ENCRYPTION_KEY=your-encryption-key
```

### Database Configuration

The production database runs on Amazon RDS PostgreSQL 17.4 with automated backups and monitoring enabled. Connection details are stored in environment variables for security.

### API Configuration

The REST API is hosted on AWS API Gateway with Lambda integration. CORS is configured for cross-origin requests from the frontend applications.

### Email Configuration

SendGrid integration handles all email communications including user invitations, notifications, and administrative messages.

## 📊 Current Database Status

- **Host**: peer-bridge-production-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
- **Port**: 5432
- **Records**: 6 invitation records (2 accepted, 4 pending)
- **Status**: ✅ Operational

## 🚀 API Documentation

### Endpoints

#### Get Dashboard Statistics
```http
GET /api/dashboard-stats
```

**Response:**
```json
{
  "totalInvitationsSent": 6,
  "totalUsersRegistered": 2,
  "pendingInvitations": 4,
  "invitationErrors": 0
}
```

#### Send Invitation
```http
POST /api/email
Content-Type: application/json

{
  "firstName": "John",
  "lastName": "Doe",
  "email": "john.doe@example.com",
  "role": "entrepreneur"
}
```

#### List Invitations
```http
GET /api/invitations
```

## 🔒 Security Considerations

All sensitive data is encrypted at rest and in transit. Database access is restricted through VPC security groups. API endpoints implement proper authentication and authorization where required.

### Planned Security Enhancements
- Background checks for all users (SSN verification for US users)
- Multi-factor authentication (MFA)
- Advanced rate limiting and DDoS protection

## 📈 Monitoring and Logging

CloudWatch Logs capture all Lambda function execution details and API Gateway access logs. Database performance metrics are monitored through RDS CloudWatch integration.

## 🤝 Contributing

This is a proprietary project owned by Spinovation. For internal development:

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Submit a pull request with detailed description
4. Ensure all CI/CD checks pass
5. Request code review from team leads

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature description"

# Push and create PR
git push origin feature/your-feature-name
```

## 📞 Support and Documentation

Additional documentation is available in the `docs/` directory including deployment guides and progress reports. For technical support, refer to the CloudWatch logs and error handling documentation.

### For Technical Issues
- Check [DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md) for deployment issues
- Review CloudWatch logs for runtime errors
- Submit issues to this GitHub repository

### For Business Questions
- Contact: support@peerbridge.ai
- Website: https://peerbridge.ai

## 📄 License

This project is proprietary software owned by Spinovation. All rights reserved.

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- ✅ Basic infrastructure setup
- ✅ Sales admin dashboard
- ✅ User invitation system
- 🚧 Email integration completion

### Phase 2: Core Platform
- 📋 User registration and profiles
- 📋 Entrepreneur project listings
- 📋 Investor dashboard
- 📋 Basic matching algorithm

### Phase 3: Advanced Features
- 📋 Payment integration
- 📋 Advanced matching and recommendations
- 📋 Mobile applications
- 📋 Analytics and reporting

### Phase 4: Scale and Optimize
- 📋 Performance optimization
- 📋 Advanced security features
- 📋 International expansion
- 📋 Enterprise features

---

**Built with ❤️ by the Spinovation team**

For more information, visit [peerbridge.ai](https://peerbridge.ai)
