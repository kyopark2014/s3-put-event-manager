import json
import boto3
import os
import time
from multiprocessing import Process
from io import BytesIO
import traceback

tableName = os.environ.get('tableName')
indexName = os.environ.get('indexName')

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
    print(event)

    try:
        response = dynamodb_client.query(
            TableName=tableName,
            IndexName=indexName,
            KeyConditionExpression='event_status = :event_status',
            ExpressionAttributeValues={
                ':event_status': {'S': 'created'}
            }
        )
    except Exception:
            err_msg = traceback.format_exc()
            print('err_msg: ', err_msg)
            raise Exception ("Not able to query from dynamodb")    

    for item in response['Items']:
        print('item: ', item)

        eventId = item['event_id']['S']
        eventTimestamp = item['event_timestamp']['S']

        bucketName = item['bucket_name']['S']
        key = item['key']['S']
        print('bucketName: '+bucketName+', key: '+key)

        try:
            dynamodb_client.delete_item(
                TableName=tableName,
                ConditionExpression='event_id = :event_id and event_timestamp = :event_timestamp',
                ExpressionAttributeValues={
                    ':event_id': {'S': eventId},
                    ':eventTimestamp': {'S': eventTimestamp}
                }
            )
        except Exception:
            err_msg = traceback.format_exc()
            print('err_msg: ', err_msg)
            raise Exception ("Not able to write into dynamodb")       

    return {
        'statusCode': 200,
        # 'msg': generated_text,
    }        