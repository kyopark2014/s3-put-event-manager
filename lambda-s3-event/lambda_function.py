import json
import boto3
import os
import time
from multiprocessing import Process
from io import BytesIO
import datetime

dynamodb_client = boto3.client('dynamodb')
tableName = os.environ.get('tableName')

def lambda_handler(event, context):
    print(event)

    eventInfo = []
    for record in event['Records']:
        print("record: ", record)

        s3 = record['s3']
        bucketName = s3['bucket']['name']
        key = s3['object']['key']

        print('bucketName: '+bucketName+', key: '+key)

        eventInfo.append({
            bucketName: bucketName,
            key: key
        })

    for item in eventInfo:
        print("item: ", item)

        bucketName = item.bucketName
        key = item.key
        print('item: '+bucketName+', key: '+key)

        d = datetime.datetime.now()
        requestTime = str(d)[0:19]

        item = {
            'item_id': {'S':bucketName+bucketName},
            'bucket_name': {'S':bucketName},
            'key': {'S':key},
            'request_time': {'S':requestTime}
        }
        client = boto3.client('dynamodb')
        try:
            resp =  client.put_item(TableName=tableName, Item=item)
        except: 
            raise Exception ("Not able to write into dynamodb")        
        print('resp, ', resp)

    return {
        'statusCode': 200,
        'result': json.dumps(eventInfo),
    }        