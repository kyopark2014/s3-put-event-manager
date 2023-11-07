import json
import boto3
import os
import time
from multiprocessing import Process
from io import BytesIO
    
def lambda_handler(event, context):
    print(event)

    text = event['text']
    print('text: ', text)

    start = int(time.time())
    
    elapsed_time = int(time.time()) - start
    print("total run time(sec): ", elapsed_time)

    return {
        'statusCode': 200,
        # 'msg': generated_text,
    }        