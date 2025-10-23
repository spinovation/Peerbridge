# How to Upload ZIP File to AWS Lambda - Detailed Steps

## 🎯 Goal: Upload `lambda_function_postgresql.zip` to your Lambda function

## 📍 Step-by-Step Navigation

### **Step 1: Get to AWS Lambda Console**
1. **Open AWS Console**: https://console.aws.amazon.com/lambda/
2. **Select Region**: Make sure you're in **us-east-1** (top right corner)
3. **Click "Functions"** in the left sidebar (if not already selected)

### **Step 2: Find Your Lambda Function**
1. **Look for your function** in the list - likely named:
   - `peer-bridge-backend-v2-PeerBridgeBackendFunctionV2-kxUxfWvBwTmF`
   - Or similar with "peer-bridge-backend" in the name
2. **Click on the function name** to open it

### **Step 3: Navigate to Code Section**
1. **You'll see tabs at the top**: Configuration, Code, Test, Monitor, etc.
2. **Click on "Code" tab** (should be selected by default)
3. **You'll see the code editor** with current Lambda function code

### **Step 4: Upload the ZIP File**
1. **Look for "Upload from" button** (usually orange/blue button)
   - It's typically in the top right of the code section
   - Next to "Deploy" button
2. **Click "Upload from"** → **Select ".zip file"** from dropdown
3. **File picker will open**:
   - Browse to where you downloaded `lambda_function_postgresql.zip`
   - Select the file
   - Click "Open"

### **Step 5: Deploy the Upload**
1. **After selecting file**, you'll see:
   - File name displayed
   - Upload progress (if large file)
2. **Click "Save" or "Deploy"** button
3. **Wait for confirmation**:
   - You'll see "Successfully updated the function" message
   - Code editor will refresh with new code

## 🖼️ Visual Guide - What to Look For

### **Lambda Console Layout:**
```
┌─────────────────────────────────────────────────────────┐
│ AWS Lambda > Functions > [your-function-name]          │
├─────────────────────────────────────────────────────────┤
│ [Configuration] [Code] [Test] [Monitor] [Aliases]       │
├─────────────────────────────────────────────────────────┤
│                                    [Upload from ▼] [Deploy] │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     │ │
│ │           Code Editor Area                          │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### **Upload from Dropdown Options:**
- ✅ **.zip file** ← Select this one
- Amazon S3
- Container image

## 🚨 Important Notes

### **File Size Limit:**
- Your file is 4.2MB, which is fine
- Lambda supports up to 50MB for zip uploads
- If file is too large, you'd need to use S3

### **What Happens During Upload:**
1. AWS uploads your zip file
2. Extracts contents to Lambda environment
3. Replaces existing code
4. Updates function configuration
5. Shows success message

### **If You Don't See "Upload from" Button:**
- Make sure you're in the **Code tab**
- Scroll right if screen is narrow
- Look for **Actions** dropdown as alternative
- Try refreshing the page

## 🔍 Alternative Method (If Button Not Found)

### **Using Actions Menu:**
1. **In Code tab**, look for **"Actions"** dropdown
2. **Click Actions** → **"Upload a .zip file"**
3. **Select your file** and upload

### **Using AWS CLI (Advanced):**
```bash
aws lambda update-function-code \
  --function-name [your-function-name] \
  --zip-file fileb://lambda_function_postgresql.zip \
  --region us-east-1
```

## ✅ Verification After Upload

### **You Should See:**
1. **New code** in the editor (lambda_function.py content)
2. **Success message**: "Successfully updated the function"
3. **Updated timestamp** on the function
4. **New file structure** in the file explorer (left side)

### **Files You Should See:**
- `lambda_function.py` (main code)
- `psycopg2/` folder (database library)
- Various `.so` and `.py` files (dependencies)

## 🆘 Troubleshooting

### **Can't Find Upload Button:**
- Refresh the page
- Make sure you're in the correct function
- Check if you have permissions to modify the function

### **Upload Fails:**
- Check internet connection
- Verify file isn't corrupted
- Try uploading from different browser

### **File Too Large Error:**
- Shouldn't happen with 4.2MB file
- If it does, contact me for S3 upload method

---

**Next Step After Upload:** Set environment variables (DB_HOST, DB_NAME, etc.) in Configuration tab
