import os
import json

import boto3

from boto3.dynamodb.conditions import Attr

from modules.decimal_encoder import DecimalEncoder

dynamodb = boto3.resource('dynamodb')

def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB'])

    if not event.get("queryStringParameters"):
        result = table.scan()

        response = {
            "statusCode": 200,
            "body": json.dumps(result["Items"],
                            cls=DecimalEncoder)
        }

        return response
    else:
        size = event["queryStringParameters"].get('size')
        height = event["queryStringParameters"].get('height')

        ## fetch customers from the database ##
        if size and height:
            result = table.scan(
                FilterExpression=Attr('attributes.size').eq(size) & Attr('attributes.height').eq(int(height))
            )
        elif size and not height:
            result = table.scan(
                FilterExpression=Attr('attributes.size').eq(size)
            )
        elif height and not size:
            result = table.scan(
                FilterExpression=Attr('attributes.height').eq(int(height))
            )

        response = {
            "statusCode": 200,
            "body": json.dumps(result["Items"],
                            cls=DecimalEncoder)
        }

        return response