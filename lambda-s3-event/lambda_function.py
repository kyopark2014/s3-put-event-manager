import json
import boto3
import os
import time
from multiprocessing import Process
from io import BytesIO
    
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

    return {
        'statusCode': 200,
        'result': json.dumps(eventInfo),
    }        