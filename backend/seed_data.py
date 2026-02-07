import boto3
from datetime import datetime, timedelta
import random

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('zojacks')

# Sample data
statuses = ['active', 'pending', 'completed', 'archived']
names = [
    'Alpha Project', 'Beta Initiative', 'Gamma Task', 'Delta Workflow',
    'Epsilon Process', 'Zeta Campaign', 'Eta Module', 'Theta System',
    'Iota Feature', 'Kappa Service', 'Lambda Function', 'Mu Component',
    'Nu Integration', 'Xi Pipeline', 'Omicron Dashboard', 'Pi Analytics',
    'Rho Report', 'Sigma Metrics', 'Tau Deployment', 'Upsilon Monitor'
]

def generate_timestamp(days_ago):
    """Generate an ISO 8601 timestamp"""
    timestamp = datetime.utcnow() - timedelta(days=days_ago)
    return timestamp.isoformat() + 'Z'

def seed_data():
    """Seed sample items into DynamoDB"""
    print(f"Seeding data into table 'zojacks'...")
    
    for i in range(20):
        item = {
            'id': f'item-{i+1:03d}',
            'name': names[i],
            'status': random.choice(statuses),
            'updatedAt': generate_timestamp(random.randint(0, 30))
        }
        
        try:
            table.put_item(Item=item)
            print(f"✓ Added: {item['id']} - {item['name']}")
        except Exception as e:
            print(f"✗ Error adding {item['id']}: {str(e)}")
    
    print("\nSeeding complete!")

if __name__ == '__main__':
    seed_data()