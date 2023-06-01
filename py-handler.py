import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']

def get_emotion_handler(event, context):
    try:
        print ('Begining get_emotion_handler')
        response = dynamodb.Table(table_name).scan()
        items = response['Items']
        print ('Total items: ' + str(len(items)))
        print ('items: ' + str(items))

        while 'LastEvaluatedKey' in response:
            response = dynamodb.Table(table_name).scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items.extend(response['Items'])

        return {
            'statusCode': 200,
            'body': json.dumps({
                'data': {
                    'items': items
                },
                'message': 'Successfully retrieved all items from the database',
                'successful': True
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'data': None,
                'message': 'Failed to retrieve all items from the database, error: ' + str(e),
                'successful': False
            })
        }

def delete_emotion_handler(event, context):
    try:
        print ('Begining delete_emotion_handler')
        body = json.loads(event['body'])
        print ('body: ' + str(body))
        
        item_id = body['id']
        print ('item_id: ' + item_id)
        
        if item_id == None:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'data': None,
                    'message': 'Item ID is required',
                    'successful': False
                })
            }
            
        table = dynamodb.Table(table_name)
        print ('Begining DynamoDB delete_item')
        table.delete_item(
            Key={
                'id': item_id
            }
        )
        print ('Ending DynamoDB delete_item')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                    'data': None,
                    'message': 'Successfully deleted item from the database',
                    'successful': True
                })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'data': None,
                'message': 'Failed to delete item from the database, error: ' + str(e),
                'successful': False
            })
        }
        