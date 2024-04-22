from flask import Blueprint, request, jsonify
import boto3
import uuid
import os

capsule_creation_app = Blueprint('capsule_creation_app', __name__)
aws_region = 'us-east-1'

@capsule_creation_app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  
    return response

dynamodb = boto3.resource('dynamodb', region_name=aws_region)
textract = boto3.client('textract', region_name=aws_region)
s3 = boto3.client('s3', region_name=aws_region)
sns = boto3.client('sns', region_name=aws_region)

USER_REGISTRATION_TABLE = 'UserRegistrationTable'
CAPSULE_METADATA_TABLE = 'CapsuleMetadataTable'
S3_BUCKET_NAME = 'textractimagebucket'


@capsule_creation_app.route('/create_capsule', methods=['POST'])
def create_capsule():
    # Get form data from the request
    email = request.form['email']
    delivery_date = request.form['deliveryDate']
    text_content = request.form['textContent']

    topic_prefix = f"SendCapsuleInfoTo{email.split('@')[0]}"
    sns_response = sns.list_topics()
    topics = sns_response.get('Topics', [])
    sns_topic_arn = next((topic['TopicArn'] for topic in topics if topic_prefix in topic['TopicArn']), None)
    # Get the image file from the request
    image_data = request.files['image']
    
    # Generate a unique file name for the image
    image_file_name = str(uuid.uuid4()) + os.path.splitext(image_data.filename)[1]
    
    # Save the image file in the S3 bucket
    s3.upload_fileobj(image_data, S3_BUCKET_NAME, image_file_name)
    
    # Call Amazon Textract to extract text from the image
    response = textract.detect_document_text(Document={'S3Object': {'Bucket': S3_BUCKET_NAME, 'Name': image_file_name}})
    
    # Parse the response to extract the text
    extracted_text = ''
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            extracted_text += item["Text"] + ' '
    
    # Generate a unique capsule ID
    capsule_id = str(uuid.uuid4())
    
    # Save capsule metadata in DynamoDB
    capsule_table = dynamodb.Table(CAPSULE_METADATA_TABLE)
    capsule_table.put_item(Item={
        'capsuleId': capsule_id,
        'email': email,
        'deliveryDate': delivery_date,
        'textContent': text_content,
        'extractedText': extracted_text,
        'snsTopicArn': sns_topic_arn
    })

    return jsonify({
        'capsuleId': capsule_id,
        'email': email,
        'deliveryDate': delivery_date,
        'textContent': text_content,
        'extractedText': extracted_text,
        'snsTopicArn': sns_topic_arn,
        'message': 'Capsule created successfully'
    })
