from flask import Flask, request, jsonify, Blueprint
import boto3


login_handler_app = Blueprint('login_handler_app', __name__)

app = Flask(__name__)


@login_handler_app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  
    return response

aws_region = 'us-east-1'

# AWS configuration
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table_name = 'UserRegistrationTable'
sns = boto3.client('sns', region_name=aws_region)


@login_handler_app.route('/login', methods=['POST'])
def login():
    try:
        # Parse the request data
        login_data = request.get_json()
        email = login_data.get('Email')
        password = login_data.get('Password')

        # Validate the request data
        if not email or not password:
            return jsonify({'message': 'Invalid request data'}), 400

        # Check if the email exists in the DynamoDB table
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'Email': email})

        if 'Item' not in response:
            # Email does not exist in DynamoDB
            return jsonify({'message': 'Email not found'}), 404

        # Verify the password
        user_data = response['Item']
        if user_data['Password'] != password:
            # Incorrect password
            return jsonify({'message': 'Incorrect password'}), 401

        # Successful login
        return handle_successful_login(email), 200

    except Exception as e:
        return jsonify({'message': 'Error occurred during login', 'error': str(e)}), 500

def handle_successful_login(email):
    clean_email = email.split('@')[0]
    topic_name = f"SendCapsuleInfoTo{clean_email}"
    
    topics_response = sns.list_topics()
    topic_exists = any(topic_name in topic['TopicArn'] for topic in topics_response['Topics'])

    if not topic_exists:
        topic_response = sns.create_topic(Name=topic_name)
        topic_arn = topic_response['TopicArn']
        subscription_response = sns.subscribe(
            TopicArn=topic_arn,
            Protocol='email',
            Endpoint=email
        )
        
        return {
            'message': 'Login successful',
            'sns_topic_arn': topic_arn,
            'subscription_arn': subscription_response['SubscriptionArn']
        }
    else:
        return jsonify({'message': 'Login successful'})
    


"""
All references:
    Flask - (Creating first simple application)
    Reference: `Flask in Python Documentation <https://www.geeksforgeeks.org/flask-creating-first-simple-application//>`_

    Enable Flask-CORS in Python
    Reference: `Flask-CORS in Python Documentation <https://www.geeksforgeeks.org/how-to-install-flask-cors-in-python/>`_

    Add data to Cloud Firestore
    Reference: `Firestore Documentation <https://firebase.google.com/docs/firestore/manage-data/add-data>`_

    Get data with Cloud Firestore
    Reference: `Firestore Documentation <https://firebase.google.com/docs/firestore/query-data/get-data>`_

    How to Get the Current Time in Python with Datetime
    Reference: `freeCodeCamp.org <https://www.freecodecamp.org/news/how-to-get-the-current-time-in-python-with-datetime>`_

"""