import json
import boto3
import os
import datetime
import uuid

tableName = os.environ.get('tableName')

def lambda_handler(event, context):
    print(event)

    s3eventInfo = []
    for record in event['Records']:
        print("record: ", record)

        s3 = record['s3']
        bucketName = s3['bucket']['name']
        key = s3['object']['key']

        print('bucketName: '+bucketName+', key: '+key)

        eventId = uuid.uuid1()
        print('eventId: ', eventId)

        d = datetime.datetime.now()
        timestamp = str(d)[0:19]        
        
        item = {
            'event_id': {'S':eventId},
            'event_timestamp': {'S':timestamp},
            'event_status': {'S':'created'},  
            'bucket_name': {'S':bucketName},
            'key': {'S':key}
        }
        
        client = boto3.client('dynamodb')
        try:
            resp = client.put_item(TableName=tableName, Item=item)
        except: 
            raise Exception ("Not able to write into dynamodb")        
        print('resp, ', resp)

        s3eventInfo.append({
            'bucketName': bucketName,
            'key': key
        })
        
    return {
        'statusCode': 200,
        'result': json.dumps(s3eventInfo),
    }        