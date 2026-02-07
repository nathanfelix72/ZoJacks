# ZoJacks

Minimal web app: React frontend fetches from a Lambda Function URL (Python) that reads from DynamoDB. No API Gateway.

## Goal

Single HTTP endpoint that returns JSON. React displays it. That's it—no auth, no writes, no complex routing.

## Architecture

```
React → HTTP GET → Lambda (Python) → DynamoDB
```

```
┌─────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   React     │────▶│  Lambda Function    │────▶│    DynamoDB         │
│  Frontend   │ GET │  (Function URL)     │     │  Table: zojacks     │
└─────────────┘     └─────────────────────┘     └─────────────────────┘
```

## Setup

### Prerequisites

AWS CLI, Node.js, Python 3.x

### DynamoDB

Create table `zojacks` with partition key `id` (string). Attributes: `id`, `name`, `status`, `updatedAt` (ISO 8601).

**CLI:**
```bash
aws dynamodb create-table --table-name zojacks \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region us-west-1
```

### Seed Data

```bash
pip install boto3
python backend/seed_data.py
```

Seeds ~20 items (item-001 through item-020) with various statuses.

### Lambda

1. Create function `zojacksPython`, Python 3.12
2. Attach `AmazonDynamoDBReadOnlyAccess` to the role
3. Deploy `lambda_function.py`
4. Create Function URL (auth: NONE). Don't enable CORS in config—handled in code.

### Frontend

```bash
cd frontend/zojacks-frontend
npm install
```

Set `LAMBDA_URL` in `App.js`, then `npm start`. Runs at localhost:3000.

## API

**Endpoint:** `GET https://hjbob2m5hztyrl2lov3nmdf7mq0hcktw.lambda-url.us-west-1.on.aws/`

**Query params:** `limit` (optional, default 25, max 100)

**Example:**
```bash
curl "https://hjbob2m5hztyrl2lov3nmdf7mq0hcktw.lambda-url.us-west-1.on.aws/?limit=10"
```

**Response:**
```json
{
  "items": [{ "id": "string", "name": "string", "status": "string", "updatedAt": "ISO 8601" }],
  "count": 10
}
```

## Cost

Stays within Free Tier. Lambda + DynamoDB on-demand + Function URL = $0 for typical usage. No EC2, RDS, ALB, NAT, or paid messaging.

## Project Structure

```
├── backend/
│   ├── lambda_function.py
│   └── seed_data.py
├── frontend/zojacks-frontend/
└── README.md
```
