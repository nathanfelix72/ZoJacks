import json
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('zojacks')

# Helper to convert DynamoDB Decimal types to standard Python types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    """
    Lambda function to query DynamoDB and return items as JSON
    Supports optional 'limit' query parameter (default 25, max 100)
    """
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, OPTIONS'
    }
    
    try:
        # Handle OPTIONS request for CORS preflight
        if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        # Get limit from query parameters (default 25, max 100)
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 25))
        
        # Enforce maximum limit of 100
        if limit > 100:
            limit = 100
        if limit < 1:
            limit = 1
        
        # Scan the table (since we're getting all items, not querying by key)
        response = table.scan(Limit=limit)
        
        items = response.get('Items', [])
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                'items': items,
                'count': len(items)
            }, cls=DecimalEncoder)
        }
        
    except Exception as e:
        # Return error response
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }