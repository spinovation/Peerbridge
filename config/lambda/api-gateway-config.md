# API Gateway Configuration

## API Details
- **API Name**: peer-bridge-backend-v2
- **API Type**: REST API
- **Region**: us-east-1
- **Stage**: Prod
- **Endpoint**: https://0vdnf29o06.execute-api.us-east-1.amazonaws.com/Prod

## Resource Structure
```
/
├── /api
    ├── /dashboard-stats (GET)
    ├── /invitations (GET, DELETE)
    ├── /email (POST)
    ├── /send-invitation (POST)
    ├── /accept-invitation (POST)
    └── /users (GET, POST, PUT, DELETE)
        └── /{userId}
            ├── /reset-password (POST)
            └── (PUT, DELETE)
```

## CORS Configuration
```json
{
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
}
```

## Method Configuration

### GET /api/dashboard-stats
- **Integration**: Lambda Function
- **Lambda Function**: peer-bridge-backend-v2-PeerBridgeBackendFunctionV2
- **Authorization**: None
- **API Key Required**: No

### POST /api/email
- **Integration**: Lambda Function
- **Lambda Function**: peer-bridge-backend-v2-PeerBridgeBackendFunctionV2
- **Authorization**: None
- **API Key Required**: No
- **Request Body**: JSON

### GET /api/invitations
- **Integration**: Lambda Function
- **Lambda Function**: peer-bridge-backend-v2-PeerBridgeBackendFunctionV2
- **Authorization**: None
- **API Key Required**: No

## Deployment Configuration
- **Stage Name**: Prod
- **Stage Description**: Production deployment
- **Deployment Description**: Latest deployment
- **Cache Settings**: Disabled
- **Throttling**: 
  - Rate: 1000 requests per second
  - Burst: 2000 requests

## Monitoring
- **CloudWatch Logs**: Enabled
- **Access Logging**: Enabled
- **Execution Logging**: INFO level
- **Data Trace**: Disabled
- **Metrics**: Enabled

## Security
- **API Key**: Not required (public API)
- **Authorization**: None (consider adding in future)
- **Resource Policy**: None
- **WAF**: Not configured
- **Certificate**: Default API Gateway certificate

## Custom Domain (Future)
- **Domain Name**: api.peerbridge.ai
- **Certificate**: ACM certificate
- **Base Path Mapping**: /v1 -> Prod stage

## Rate Limiting
- **Default Throttling**: 10,000 requests per second
- **Burst**: 5,000 requests
- **Per-Client**: 1,000 requests per second

## Request/Response Transformation
- **Request Templates**: None
- **Response Templates**: None
- **Request Validation**: Basic validation
- **Response Headers**: CORS headers added

## Error Handling
- **Gateway Responses**: Default 4xx and 5xx responses
- **Custom Error Pages**: Not configured
- **Error Logging**: Enabled in CloudWatch
