from flask import Flask, request, jsonify, Blueprint
import boto3

app = Flask(__name__)
# CORS(app)

registration_handler_app = Blueprint('registration_handler_app', __name__)


@registration_handler_app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Headers", "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers")
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")  # Add the allowed methods here
    return response

aws_region = 'us-east-1'

# AWS configuration
dynamodb = boto3.resource('dynamodb', region_name=aws_region)
table_name = 'UserRegistrationTable'

sns = boto3.client('sns', region_name=aws_region)

@registration_handler_app.route('/register', methods=['POST'])
def register():
    try:
        # Parse the request data
        registration_data = request.get_json()
        name = registration_data.get('Name')
        password = registration_data.get('Password')
        email = registration_data.get('Email')

        print(registration_data)
        # Validate the request data
        if not name or not password or not email:
            return jsonify({'message': 'Invalid request data'}), 400

        # Check if the email already exists in the DynamoDB table
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'Email': email}) #when using get_item(), need to specify both PARTITION key and SORT key(if mentioned in schema)

        if 'Item' in response:
            # Item exists in DynamoDB
            return jsonify({'message': 'Email already exists'}), 409

        # Add the registration information to the DynamoDB table
        table.put_item(Item={'Name': name, 'Password': password, 'Email': email})


        # Return a success response
        return jsonify({'message': 'Registration successful'}), 200

    except Exception as e:
        return jsonify({'message': 'Error occurred during registration', 'error': str(e)}), 500
