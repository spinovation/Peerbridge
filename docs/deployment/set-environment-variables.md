# Set Environment Variables - Lambda Configuration

## 🎯 Goal: Configure database connection for your Lambda function

## 📍 Exact Navigation Steps

### **Step 1: Navigate to Configuration**
1. **In your Lambda function console** (where you just uploaded the code)
2. **Click "Configuration" tab** - it's next to the "Code" tab at the top
3. **Look for left sidebar** with options like "General configuration", "Environment variables", etc.

### **Step 2: Access Environment Variables**
1. **Click "Environment variables"** in the left sidebar
2. **You'll see current environment variables** (probably empty or just a few)
3. **Click "Edit" button** (usually orange/blue button)

### **Step 3: Add Database Variables**

**Click "Add environment variable" and add each of these:**

#### **Variable 1:**
- **Key:** `DB_HOST`
- **Value:** `peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com`

#### **Variable 2:**
- **Key:** `DB_NAME`
- **Value:** `peerbridge`

#### **Variable 3:**
- **Key:** `DB_USER`
- **Value:** `postgres`

#### **Variable 4:**
- **Key:** `DB_PASSWORD`
- **Value:** `!Q2w3e4r5t`

#### **Variable 5:**
- **Key:** `DB_PORT`
- **Value:** `5432`

### **Step 4: Save Configuration**
1. **Click "Save"** button after adding all variables
2. **Wait for confirmation** - you'll see "Successfully updated environment variables"

## 🖼️ Visual Guide

### **Configuration Tab Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ [Configuration] [Code] [Test] [Monitor]                 │
├─────────────────────────────────────────────────────────┤
│ Left Sidebar:           │ Main Area:                    │
│ • General configuration │ Environment Variables         │
│ • Environment variables │ ┌─────────────────────────┐   │
│ • Tags                  │ │ Key      │ Value        │   │
│ • Execution role        │ │ DB_HOST  │ peerbridge...│   │
│ • VPC                   │ │ DB_NAME  │ peerbridge  │   │
│ • Monitoring            │ │ DB_USER  │ postgres    │   │
│                         │ │ DB_PASSWORD │ !Q2w3e4r5t │   │
│                         │ │ DB_PORT  │ 5432        │   │
│                         │ └─────────────────────────┘   │
│                         │           [Save]              │
└─────────────────────────────────────────────────────────┘
```

## ⚠️ Important Notes

### **Case Sensitivity:**
- Variable names are **case-sensitive**
- Use exactly: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_PORT`

### **No Quotes Needed:**
- Don't add quotes around values
- Just paste the values directly

### **Password Security:**
- The password will be encrypted by AWS
- It won't be visible in plain text after saving

## ✅ Verification Steps

### **After Saving Environment Variables:**
1. **Go back to your Sales Admin dashboard**
2. **Refresh the page** (Ctrl+F5 or Cmd+Shift+R)
3. **Check if "Error" is replaced with numbers**

### **Expected Results:**
- **Total Invitations Sent:** Should show a number (like 6)
- **Users Registered:** Should show a number (like 2)  
- **Pending Invitations:** Should show a number (like 4)
- **Invitation Errors:** Should show 0

## 🔍 Troubleshooting

### **If Still Showing "Error":**
1. **Check CloudWatch Logs:**
   - Go to "Monitor" tab in Lambda
   - Click "View CloudWatch logs"
   - Look for recent error messages

2. **Common Issues:**
   - Typo in environment variable names
   - Wrong database endpoint
   - Database security group not allowing Lambda access

### **If Database Connection Fails:**
- The code has fallback to sample data
- You should at least see some numbers instead of "Error"
- Check VPC and security group settings

## 🚀 Next Steps After Success

1. **Test invitation creation** - try sending a single invitation
2. **Verify data persistence** - check if new invitations appear in the table
3. **Test search functionality** - use the date filters
4. **Clean up duplicate resources** - as discussed earlier

---

**Expected Time:** 5-10 minutes  
**Expected Outcome:** Sales Admin dashboard shows real database statistics
