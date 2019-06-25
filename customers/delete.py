import os
import json

import boto3

dynamodb = boto3.resource('dynamodb')

def delete(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB'])

    ## delete the customer from the database ##
    table.delete_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    response = {
        "statusCode": 200,
        "body": json.dumps({"success": True})
    }

    return response