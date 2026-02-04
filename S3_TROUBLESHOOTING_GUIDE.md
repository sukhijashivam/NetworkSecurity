# S3 Bucket Upload Troubleshooting Guide

## Problem: S3 Bucket is Empty

Your S3 bucket is empty despite running the training pipeline. Here are the likely causes and solutions:

---

## 1. **AWS Credentials Not Configured**

### Symptoms:
- S3 sync commands fail silently
- No files appear in S3 bucket

### Solution:
Run these commands in your terminal:

```bash
# Configure AWS credentials
aws configure

# When prompted, enter:
# AWS Access Key ID: [your_access_key]
# AWS Secret Access Key: [your_secret_key]
# Default region name: us-east-1 (or your region)
# Default output format: json
```

### Verify:
```bash
# Test S3 access
aws s3 ls

# List your bucket
aws s3 ls s3://your-bucket-name
```

---

## 2. **TRAINING_BUCKET_NAME Not Set**

### Check in Code:
Open [networksecurity/constant/training_pipeline/__init__.py](networksecurity/constant/training_pipeline/__init__.py)

Look for:
```python
TRAINING_BUCKET_NAME = "your-s3-bucket-name"
```

### If Missing:
Add this line to the constants file with your actual S3 bucket name.

---

## 3. **Local Artifact Directories Not Created**

### Symptoms:
- Syncing fails because local folders don't exist

### Check:
```bash
# In your project directory, check if these exist:
ls -la artifacts/  # artifact directory
ls -la final_model/  # model directory
```

### Solution:
The pipeline should create these automatically. If not:
```bash
mkdir -p artifacts
mkdir -p final_model
```

---

## 4. **AWS Permissions Issues**

### Check Bucket Policy:
Your AWS S3 bucket must allow your IAM user to write. Verify:

1. Go to AWS Console → S3 → Your Bucket
2. Click **Permissions** tab
3. Check **Bucket Policy** allows `s3:PutObject`, `s3:GetObject`, etc.

### Required Permissions:
```json
{
    "Effect": "Allow",
    "Principal": {
        "AWS": "arn:aws:iam::YOUR_ACCOUNT_ID:user/YOUR_USER"
    },
    "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:DeleteObject"
    ],
    "Resource": [
        "arn:aws:s3:::your-bucket-name",
        "arn:aws:s3:::your-bucket-name/*"
    ]
}
```

---

## 5. **Check Training Logs for Errors**

### View Recent Logs:
```bash
# Go to logs directory
cd logs/

# View the most recent log file
cat [latest_log_file].log | tail -100
```

### Look for Lines Like:
```
ERROR: Failed to sync artifacts to S3
ERROR: S3 sync failed: Access Denied
```

---

## 6. **Verify AWS CLI is Installed**

```bash
# Check AWS CLI version
aws --version

# If not installed:
pip install awscli
```

---

## 7. **Test S3 Upload Manually**

```bash
# Create a test file
echo "test" > test.txt

# Upload to your bucket
aws s3 cp test.txt s3://your-bucket-name/test.txt

# Verify
aws s3 ls s3://your-bucket-name/
```

---

## Recent Improvements Made

✅ **Enhanced S3 Syncer** ([s3_syncer.py](networksecurity/cloud/s3_syncer.py)):
- Added proper error logging and subprocess handling
- Now captures and displays S3 sync errors
- Checks if local directories exist before syncing
- Uses subprocess instead of os.system for better error handling

✅ **Improved Pipeline Error Handling** ([training_pipeline.py](networksecurity/pipeline/training_pipeline.py)):
- S3 sync failures now log warnings instead of crashing
- Pipeline completes training even if S3 upload fails
- Better logging for debugging S3 issues

---

## Debug Steps

Run these commands to diagnose:

```bash
# 1. Check if AWS configured
aws sts get-caller-identity

# 2. List your buckets
aws s3 ls

# 3. Check artifact directory
ls -la artifacts/

# 4. Try manual sync
aws s3 sync artifacts/ s3://your-bucket-name/test/

# 5. Check logs during training
tail -f logs/[latest].log
```

---

## After Fixing:

1. Restart the app:
```bash
python app.py
```

2. Visit: `http://localhost:8000/train`

3. Check logs for S3 upload messages

4. Verify in AWS Console → S3 → Your Bucket

---

## Support Variables

Check that these are set in your environment:
- `MONGODB_URL_KEY` - MongoDB connection string
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `TRAINING_BUCKET_NAME` - Your S3 bucket name

