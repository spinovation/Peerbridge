# CloudFormation Cleanup Guide - PeerBridge.ai

## Current Stack Analysis

Based on the CloudFormation console screenshot, here's the cleanup plan:

### **Stack Inventory (4 total)**

| Stack Name | Created | Status | Action | Reason |
|------------|---------|--------|--------|---------|
| `peer-bridge-backend-v2` | Oct 9, 21:23 | UPDATE_COMPLETE | **KEEP** | Most recent, likely active |
| `peer-bridge-backend` | Oct 7, 13:11 | UPDATE_COMPLETE | **DELETE** | Superseded by v2 |
| `peer-bridge-backend-5efe4f27-CompanionStack` | Oct 7, 15:06 | UPDATE_COMPLETE | **DELETE** | ECR companion stack |
| `aws-sam-cli-managed-default` | Oct 7, 15:05 | CREATE_COMPLETE | **KEEP** | SAM infrastructure |

## Cleanup Steps

### **Step 1: Verify Active Resources (CRITICAL)**
Before deleting anything, verify which stack contains your active Lambda:

1. Go to **API Gateway Console**
2. Find your API: `https://0vdnf29o06.execute-api.us-east-1.amazonaws.com`
3. Check which Lambda function it points to
4. Note the Lambda function name/ARN
5. Cross-reference with CloudFormation stacks to confirm which stack is active

### **Step 2: Safe Deletion Order**

#### **Delete First: `peer-bridge-backend-5efe4f27-CompanionStack`**
- **Purpose**: ECR repository for container images
- **Risk**: Low - can be recreated if needed
- **Action**: Delete this stack first

#### **Delete Second: `peer-bridge-backend`** 
- **Purpose**: Original backend stack (superseded by v2)
- **Risk**: Medium - verify it's not serving your API first
- **Action**: Delete only after confirming v2 is active

### **Step 3: Keep These Stacks**

#### **Keep: `peer-bridge-backend-v2`**
- **Purpose**: Current backend infrastructure
- **Contains**: Your active Lambda function (likely)
- **Action**: Keep and use for database integration update

#### **Keep: `aws-sam-cli-managed-default`**
- **Purpose**: AWS SAM CLI managed resources
- **Contains**: Default S3 buckets and IAM roles for SAM deployments
- **Action**: Keep for future deployments

## Verification Commands

After cleanup, verify you have the right resources:

```bash
# Check active Lambda functions
aws lambda list-functions --region us-east-1

# Check API Gateway integrations
aws apigateway get-rest-apis --region us-east-1

# Verify RDS instances (should only be 1)
aws rds describe-db-instances --region us-east-1
```

## Expected Result

After cleanup:
- **2 CloudFormation stacks** (down from 4)
- **1 Lambda function** (serving your API)
- **1 RDS database** (`peerbridge-db`)
- **Clean, manageable infrastructure**

## Risk Mitigation

1. **Take screenshots** of current working API Gateway configuration
2. **Note down** the exact Lambda function ARN that's working
3. **Test API endpoints** before and after each deletion
4. **Have rollback plan**: Keep the deployment package ready to redeploy if needed

## Cost Savings

Removing duplicate stacks will save:
- Duplicate Lambda function costs (minimal but clean)
- Unused CloudFormation stack management overhead
- Clearer resource inventory for future development
