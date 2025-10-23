# GitHub Repository Setup Guide

This guide will help you push the complete PeerBridge repository to GitHub at https://github.com/spinovation/PeerbridgeSandbox.

## Prerequisites

1. **GitHub Account**: Ensure you have access to the `spinovation` GitHub organization
2. **Git Configured**: Make sure Git is configured with your credentials
3. **Repository Access**: You should have admin access to the PeerbridgeSandbox repository

## Step 1: Verify Git Configuration

```bash
# Check your Git configuration
git config --global user.name
git config --global user.email

# If not configured, set them up
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## Step 2: Initialize Git Repository

```bash
# Navigate to the PeerbridgeSandbox directory
cd /home/ubuntu/PeerbridgeSandbox

# Initialize Git repository
git init

# Add the GitHub remote
git remote add origin https://github.com/spinovation/PeerbridgeSandbox.git

# Check if remote was added correctly
git remote -v
```

## Step 3: Prepare Files for Commit

```bash
# Create .gitignore file
cat > .gitignore << 'EOF'
# Environment files with secrets
config/environment/production.env
config/environment/development.env
*.env

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp

# AWS
.aws/
aws-exports.js

# Node modules (if any)
node_modules/

# Lambda deployment packages
*.zip
lambda-deployment.zip

# Database dumps
*.sql.backup
*.dump

# Screenshots (optional - you may want to keep some)
assets/screenshots/*.png

# Recovery files
upload/.recovery/
EOF
```

## Step 4: Create Environment Template

```bash
# Create template for production environment
cp config/environment/production.env config/environment/production.env.example

# Replace sensitive values with placeholders in the example file
sed -i 's/bxWSK7fWIHKDllrc0vVc/your-secure-database-password/g' config/environment/production.env.example
sed -i 's/your_sendgrid_api_key_here/your-sendgrid-api-key/g' config/environment/production.env.example
sed -i 's/your_jwt_secret_key_here/your-jwt-secret-key/g' config/environment/production.env.example
sed -i 's/your_encryption_key_here/your-encryption-key/g' config/environment/production.env.example
```

## Step 5: Add and Commit Files

```bash
# Add all files to staging
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: Complete PeerBridge repository structure

- Add AWS infrastructure CloudFormation templates
- Add Lambda function with PostgreSQL integration
- Add Sales Admin dashboard frontend
- Add comprehensive database schema
- Add deployment documentation
- Add environment configuration templates
- Add project documentation and README"
```

## Step 6: Push to GitHub

```bash
# Push to GitHub (you may need to authenticate)
git push -u origin main

# If the repository already exists and you need to force push
# git push -u origin main --force
```

## Step 7: Set Up Repository Settings

After pushing, configure the repository on GitHub:

### Repository Description
```
PeerBridge.ai - Invitation-only professional networking platform connecting entrepreneurs, investors, and affiliates for smarter funding and collaborative business building.
```

### Topics/Tags
Add these topics to help with discoverability:
- `aws`
- `lambda`
- `postgresql`
- `serverless`
- `networking`
- `investment`
- `entrepreneurship`
- `python`
- `cloudformation`

### Branch Protection (Recommended)
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews before merging
   - Require status checks to pass before merging
   - Restrict pushes to matching branches

### Secrets Configuration
Add these secrets for CI/CD (Settings → Secrets and variables → Actions):

```
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_REGION=us-east-1
DATABASE_PASSWORD=your-secure-password
SENDGRID_API_KEY=your-sendgrid-api-key
```

## Step 8: Verify Repository Structure

After pushing, verify the repository structure on GitHub:

```
✅ README.md (with badges and comprehensive documentation)
✅ frontend/sales-admin/index.html (Sales Admin dashboard)
✅ backend/lambda-functions/main.py (Lambda function)
✅ database/schema.sql (Database schema)
✅ infrastructure/cloudformation/ (AWS templates)
✅ config/environment/ (Configuration templates)
✅ docs/deployment/ (Deployment guides)
✅ .gitignore (Proper exclusions)
```

## Step 9: Create Initial Release

Create a release to mark the initial version:

1. Go to Releases → Create a new release
2. Tag version: `v1.0.0`
3. Release title: `Initial Release - PeerBridge Foundation`
4. Description:
```markdown
## 🚀 PeerBridge v1.0.0 - Foundation Release

This is the initial release of PeerBridge.ai, featuring a complete serverless architecture on AWS.

### ✨ Features
- **Sales Admin Dashboard**: Complete invitation management system
- **AWS Infrastructure**: CloudFormation templates for full deployment
- **Database Schema**: PostgreSQL schema with comprehensive tables
- **Lambda API**: Python 3.11 backend with database integration
- **Documentation**: Complete deployment and setup guides

### 🏗️ Infrastructure
- AWS Lambda + API Gateway
- RDS PostgreSQL 17.4
- S3 static hosting
- SendGrid email integration
- CloudFormation IaC

### 📊 Current Status
- 6 invitation records in production database
- Sales Admin dashboard operational
- API endpoints functional
- Ready for production deployment

### 🚀 Quick Start
See [DEPLOYMENT.md](docs/deployment/DEPLOYMENT.md) for complete setup instructions.
```

## Troubleshooting

### Authentication Issues
If you encounter authentication issues:

```bash
# Use GitHub CLI (if installed)
gh auth login

# Or use personal access token
git remote set-url origin https://your-username:your-token@github.com/spinovation/PeerbridgeSandbox.git
```

### Large File Issues
If you encounter large file warnings:

```bash
# Check file sizes
find . -type f -size +50M

# Remove large files and add to .gitignore if needed
git rm --cached large-file.zip
echo "large-file.zip" >> .gitignore
```

### Repository Already Exists
If the repository already has content:

```bash
# Pull existing content first
git pull origin main --allow-unrelated-histories

# Resolve any conflicts, then push
git push origin main
```

## Next Steps

After successfully pushing to GitHub:

1. **Update API URLs**: Replace placeholder URLs in frontend with actual API Gateway URLs
2. **Configure CI/CD**: Set up GitHub Actions for automated deployment
3. **Add Team Members**: Invite collaborators to the repository
4. **Create Issues**: Add GitHub issues for known bugs and feature requests
5. **Set up Project Board**: Create GitHub project board for task management

## Security Notes

- Never commit actual passwords or API keys
- Use GitHub Secrets for sensitive CI/CD variables
- Regularly rotate access tokens and passwords
- Enable 2FA on all GitHub accounts with access

## Support

If you encounter issues with the GitHub setup:
1. Check GitHub's documentation on repository setup
2. Verify your permissions on the spinovation organization
3. Contact GitHub support if needed
4. Review Git documentation for troubleshooting commands
