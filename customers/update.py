import os
import json

import boto3

from botocore.exceptions import ClientError

from modules.decimal_encoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')

def update(event, context):
    messages = []
    request = json.loads(event['body'])

    if 'first_name' not in request:
        messages.append("Customer first name is required")
    if 'last_name' not in request:
        messages.append("Customer last name is required")
    if 'gender' not in request:
        messages.append("Customer gender is required")
    if 'country' not in request:
        messages.append("Customer country is required")
    if 'attributes' not in request:
        messages.append("Customer attributes is required - size, height")

    if messages:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": ". ".join(messages)
            })
        }

    table = dynamodb.Table(os.environ['DYNAMODB'])

    ## update the todo in the database ##
    try:
        result = table.update_item(
            Key={
                'id': event['pathParameters']['id']
            },
            UpdateExpression='SET first_name = :fn, '
                            'last_name = :ln, '
                            'gender = :g, '
                            'country = :c, '
                            'attributes.size = :s, '
                            'attributes.height = :h ',
            ExpressionAttributeValues={
            ':fn': request['first_name'],
            ':ln': request['last_name'],
            ':g': request['gender'],
            ':c': request['country'],
            ':s': request["attributes"].get("size"),
            ':h': request["attributes"].get("height")
            },
            ReturnValues='ALL_NEW',
        )
    except ClientError as e:
        return {
            "statusCode": 409,
            "body": json.dumps({
                "message": f"{e.response['Error']['Message']}"
            })
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(
            result['Attributes'],
            cls=DecimalEncoder
        )
    }

    return response