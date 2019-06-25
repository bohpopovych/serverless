import json
import os
import uuid

import boto3

dynamodb = boto3.resource('dynamodb')

def create(event, context):
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

    customer = {
        'id': str(uuid.uuid1()),
        'first_name': request['first_name'],
        'last_name': request['last_name'],
        'gender': request['gender'],
        'country': request['country'],
        'attributes': {
            'size': request["attributes"].get("size"),
            'height': request["attributes"].get("height")
        }
    }

    ## save a new customer to the database ##
    table.put_item(Item=customer)

    response = {
        "statusCode": 200,
        "body": json.dumps(customer)
    }

    return response
