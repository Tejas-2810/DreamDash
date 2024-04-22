# This module would manage scheduling the delivery of capsules using AWS EventBridge based on the specified delivery date.

# Key Functions:
# schedule_capsule_delivery(capsule_id, delivery_date): Creates an EventBridge rule to trigger capsule delivery at the specified date

import boto3
import json
import logging
from datetime import datetime, timedelta

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS SDK clients
eventbridge = boto3.client('events')
lambda_client = boto3.client('lambda')
HALIFAX_TIME_DIFFERENCE_HOURS = -3

def lambda_handler(event, context):
    processed_records = []
    region = context.invoked_function_arn.split(":")[3]
    account_id = context.invoked_function_arn.split(":")[4]
    
    for record in event['Records']:
        # Process only 'INSERT' events
        if record['eventName'] == 'INSERT':
            new_image = record['dynamodb']['NewImage']
            
            capsule_id = new_image['capsuleId']['S']
            delivery_date = new_image['deliveryDate']['S']
            user_id = new_image['email']['S']

            cron_expression = convert_date_to_cron(delivery_date)

            rule_name = f'CapsuleDelivery-{capsule_id}'

            rule_arn = f'arn:aws:events:{region}:{account_id}:rule/{rule_name}'
            try:
                # Create the EventBridge rule
                eventbridge.put_rule(
                    Name=rule_name,
                    ScheduleExpression=cron_expression,
                    State='ENABLED',
                    Description=f'Deliver capsule {capsule_id} to user {user_id}'
                )
                # give the arn for delivery lambda
                target_arn = 'arn:aws:lambda:us-east-1:645019798228:function:CapsuleDeliveryLambda'
                
                eventbridge.put_targets(
                    Rule=rule_name,
                    Targets=[{
                        'Id': f'TargetFor-{capsule_id}',
                        'Arn': target_arn,
                        'Input': json.dumps({
                            'capsuleId': capsule_id,
                        })
                    }]
                )

                add_invoke_permission(target_arn, rule_arn)

                processed_records.append({
                    'capsuleId': capsule_id,
                    'ruleName': rule_name,
                    'status': 'Success'
                })
                
                logger.info(f"Successfully created rule {rule_name} for capsule {capsule_id}")

            except Exception as e:
                logger.error(f"Error creating rule for capsule {capsule_id}: {e}")
                processed_records.append({
                    'capsuleId': capsule_id,
                    'ruleName': rule_name,
                    'status': 'Error',
                    'error': str(e)
                })

    return {
        'processedRecords': processed_records
    }

def add_invoke_permission(lambda_arn, rule_arn):
    try:
        rule_name_part = rule_arn.split('/')[-1]
        statement_id = f"EventBridgeInvoke-{rule_name_part}".replace('/', '-').replace(':', '-')
        lambda_client.add_permission(
            FunctionName=lambda_arn,
            StatementId=statement_id,
            Action='lambda:InvokeFunction',
            Principal='events.amazonaws.com',
            SourceArn=rule_arn
        )
        logger.info(f"Invoke permission added for {lambda_arn} with rule {rule_arn}")
    except lambda_client.exceptions.ResourceConflictException:
        logger.info(f"Permission already exists for {lambda_arn} with rule {rule_arn}")
    except Exception as e:
        logger.error(f"Error adding invoke permission for {lambda_arn}: {e}")


def convert_date_to_cron(delivery_date):
    # Parse the delivery_date string into a datetime object
    date_time_obj = datetime.fromisoformat(delivery_date)

    adjusted_date_time_obj = date_time_obj + timedelta(hours=3)

    # Extract year, month, day, hour, and minute components
    year = adjusted_date_time_obj.year
    month = adjusted_date_time_obj.month
    day = adjusted_date_time_obj.day
    hour = adjusted_date_time_obj.hour
    minute = adjusted_date_time_obj.minute

    # Construct the cron expression (minute, hour, day of month, month, day of week, year)
    cron_expression = f'cron({minute} {hour} {day} {month} ? {year})'

    return cron_expression
    