import json
import urllib.parse
import boto3

s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    real_key = event['Records'][0]['s3']['object']['key']
    textract_client = boto3.client('textract')
    response = textract_client.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': "orsstorage1",
                'Name': "image.png"
            }
        })
    s3_client.delete_object(Bucket=bucket, Key=real_key)
    newFileName = 'createdJsonFile' + '.json'
    uploadByteStream = bytes(json.dumps(response["Blocks"]).encode('UTF-8'))
    target_bucket = 'orsstorage2'
    s3_client.put_object(Bucket=target_bucket, Key=newFileName, Body=uploadByteStream)
