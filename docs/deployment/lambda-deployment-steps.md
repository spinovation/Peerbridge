# Lambda Function Deployment Steps - PostgreSQL Integration

## 🎯 Goal
Deploy `lambda_function_postgresql.zip` to fix Sales Admin dashboard database integration

## 📋 Step-by-Step Instructions

### **Step 1: Identify Your Active Lambda Function**

1. **Go to AWS Lambda Console**
   - Navigate to: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions
   
2. **Find Your Active Function**
   - Look for the Lambda function serving your API
   - Based on your stacks, it's likely: `peer-bridge-backend-v2-PeerBridgeBackendFunctionV2-kxUxfWvBwTmF`
   - Click on the function name to open it

### **Step 2: Backup Current Function (Safety)**

1. **Download Current Code**
   - In the Lambda function console
   - Go to "Code" tab
   - Click "Actions" → "Export function" → "Download deployment package"
   - Save as backup (e.g., `lambda_backup_original.zip`)

### **Step 3: Deploy New Code**

1. **Upload New Package**
   - In the Lambda function console
   - Go to "Code" tab
   - Click "Upload from" → ".zip file"
   - Select `lambda_function_postgresql.zip`
   - Click "Save"

2. **Wait for Deployment**
   - AWS will upload and extract the package
   - Wait for "Successfully updated the function" message

### **Step 4: Configure Environment Variables**

1. **Go to Configuration Tab**
   - Click "Configuration" tab in Lambda console
   - Click "Environment variables" in left sidebar
   - Click "Edit"

2. **Add Database Variables**
   ```
   DB_HOST = peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
   DB_NAME = peerbridge
   DB_USER = postgres
   DB_PASSWORD = [your password]
   DB_PORT = 5432
   ```

3. **Optional: Add SendGrid (if you have API key)**
   ```
   SENDGRID_API_KEY = [your SendGrid API key]
   ```

4. **Save Configuration**
   - Click "Save" to apply environment variables

### **Step 5: Test the Deployment**

1. **Test API Endpoints**
   ```bash
   # Test dashboard stats
   curl "https://0vdnf29o06.execute-api.us-east-1.amazonaws.com/Prod/api/dashboard-stats"
   
   # Test invitations list
   curl "https://0vdnf29o06.execute-api.us-east-1.amazonaws.com/Prod/api/invitations"
   ```

2. **Expected Results**
   - Should return real database data instead of mock data
   - No "Error" messages in responses

### **Step 6: Test Sales Admin Dashboard**

1. **Open Dashboard**
   - Go to your Sales Admin dashboard URL
   - Login with: PBSalesAdmin / PeerBridge2025!

2. **Verify Functionality**
   - ✅ Statistics should show real numbers (not "Error")
   - ✅ Invitations table should show database data
   - ✅ "Send Single Invitation" should work
   - ✅ New invitations should be saved to database

### **Step 7: Monitor Logs (If Issues)**

1. **Check CloudWatch Logs**
   - Go to CloudWatch console
   - Find log group: `/aws/lambda/[your-function-name]`
   - Check recent log streams for any errors

2. **Common Issues & Solutions**
   - **Database connection timeout**: Check VPC/security groups
   - **Import errors**: Verify psycopg2 is included in package
   - **Environment variables**: Double-check spelling and values

## 🚨 Rollback Plan (If Something Goes Wrong)

If the deployment causes issues:

1. **Quick Rollback**
   - Go back to Lambda console
   - Upload your backup zip file (`lambda_backup_original.zip`)
   - Remove the new environment variables
   - Save and test

2. **Verify Rollback**
   - Test API endpoints return to previous behavior
   - Dashboard should work as before (with mock data)

## ✅ Success Indicators

After successful deployment:

1. **API Responses**
   ```json
   # /api/dashboard-stats should return real counts
   {
     "totalInvitationsSent": 6,
     "totalUsersRegistered": 2,
     "pendingInvitations": 4,
     "invitationErrors": 0
   }
   ```

2. **Dashboard Behavior**
   - Statistics cards show numbers (not "Error")
   - Invitations table populated with real data
   - New invitations save to database and appear in table
   - Date search filters work with real data

3. **Database Verification**
   - New `invitations` table created automatically
   - Sample data migrated to database
   - New invitations persist after Lambda restarts

## 🔧 Troubleshooting

### **If Statistics Still Show "Error"**
- Check CloudWatch logs for database connection errors
- Verify environment variables are set correctly
- Confirm database security groups allow Lambda access

### **If Invitations Table is Empty**
- Check if database initialization ran successfully
- Verify table creation in PostgreSQL
- Check for any SQL errors in logs

### **If New Invitations Don't Save**
- Check for database write permission errors
- Verify table schema matches code expectations
- Look for constraint violation errors

## 📞 Next Steps After Success

1. **Document the working configuration**
2. **Clean up duplicate resources** (as discussed)
3. **Set up monitoring/alerting** for the database connection
4. **Plan next phase** of PeerBridge development

---

**Estimated Time:** 15-30 minutes  
**Risk Level:** Low (with backup plan)  
**Expected Outcome:** Fully functional Sales Admin dashboard with real database integration
