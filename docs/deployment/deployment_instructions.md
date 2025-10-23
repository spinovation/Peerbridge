# Lambda Function Update Instructions

## Files to Deploy

1. **lambda_function_updated.py** - Replace the existing Lambda function code with this file
2. **psycopg2-binary** dependency needs to be added

## Environment Variables to Set in Lambda

Set these environment variables in your Lambda function configuration:

- `DB_HOST`: peerbridge-db.cynikc2qasyw.us-east-1.rds.amazonaws.com
- `DB_NAME`: peerbridge  
- `DB_USER`: postgres
- `DB_PASSWORD`: [the password you provided]
- `DB_PORT`: 5432
- `SENDGRID_API_KEY`: [your SendGrid API key if you have one]

## Dependencies Required

The Lambda function needs the `psycopg2-binary` package for PostgreSQL connectivity. You can either:

1. **Option 1: Add as Lambda Layer**
   - Create a Lambda layer with psycopg2-binary
   - Attach it to your function

2. **Option 2: Include in deployment package**
   - Install psycopg2-binary in a local directory
   - Zip it with your Lambda function code

## What This Update Does

1. **Connects to Real Database**: Replaces mock data with actual PostgreSQL queries
2. **Creates Tables**: Automatically creates the `invitations` table if it doesn't exist
3. **Migrates Sample Data**: Inserts the existing sample data into the database on first run
4. **Fallback Handling**: If database connection fails, falls back to sample data so the dashboard still works
5. **Maintains API Compatibility**: All existing API endpoints work exactly the same

## Testing

After deployment, test these endpoints:
- GET `/api/dashboard-stats` - Should return real database counts
- GET `/api/invitations` - Should return invitations from database
- POST `/api/email` - Should save new invitations to database

The Sales Admin dashboard will immediately start showing real data once this is deployed.
