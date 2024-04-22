import boto3
import json
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS SDK clients
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
sns = boto3.client('sns')
lambda_client = boto3.client('lambda')

# DynamoDB table and S3 bucket name - replace with your actual table and bucket names
DYNAMODB_TABLE = 'CapsuleMetadataTable'
S3_BUCKET = 'textractimagebucket'

def get_capsule_metadata(capsule_id):
    table = dynamodb.Table(DYNAMODB_TABLE)
    try:
        response = table.get_item(Key={'capsuleId': capsule_id})
        if 'Item' in response:
            return response['Item']
        else:
            print(f"No data found for capsuleId: {capsule_id}")
            return None
    except Exception as e:
        print(f"Error retrieving capsule metadata: {e}")
        return None

def send_notification(topic_arn, message):
    try:
        response = sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject='Suprise! A time capsule from your former self is waiting for you!'
        )
        return response
    except Exception as e:
        print(f"Error sending SNS notification: {e}")
        return None


def lambda_handler(event, context):
    # Extract information from the event
    capsule_id = event['capsuleId']

    # Retrieve capsule metadata
    metadata = get_capsule_metadata(capsule_id)
    if not metadata:
        return {'statusCode': 404, 'body': 'Metadata not found'}

    # Compose the notification message
    text_content = metadata.get('textContent', '')
    extracted_text = metadata.get('extractedText', '')
    message = f"{text_content}\n\nOn your success journey, I have a quick motivational quote for you:\n\n{extracted_text}"

    # Send the notification
    sns_response = send_notification(metadata['snsTopicArn'], message)
    if not sns_response:
        return {'statusCode': 500, 'body': 'Failed to send notification'}

    return {'statusCode': 200, 'body': 'Capsule delivered successfully'}
