import json
import urllib.parse
import boto3

s3_client = boto3.client('s3')

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ORS_Database')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    json_file_name = event['Records'][0]['s3']['object']['key']
    json_object = s3_client.get_object(Bucket=bucket, Key=json_file_name)
    jsonFileReader = json_object['Body'].read()
    jsonDict = json.loads(jsonFileReader)

    nameplateEntries = []
    for item in jsonDict:
        if item["BlockType"] == "LINE":
            nameplateEntries.append(item["Text"])

    table = dynamodb.Table('ORS_Database')

    if nameplateEntries[0] == 'Lieferschein':
        table.put_item(Item={'Id_Number': 1, 'Value': nameplateEntries})
        s3_client.delete_object(Bucket=bucket, Key=json_file_name)
        return 'Hello from Lambda'

    elif nameplateEntries[0] == 'WARENEINGANGSSCHEIN':
        table.put_item(Item={'Id_Number': 2, 'Value': nameplateEntries})
        s3_client.delete_object(Bucket=bucket, Key=json_file_name)
        return 'Hello from Lambda'

    elif nameplateEntries[0] == 'SIEMENS':
        table.put_item(Item={'Id_Number': 3, 'Value': nameplateEntries})
        s3_client.delete_object(Bucket=bucket, Key=json_file_name)
        return 'Hello from Lambda'

    else:
        table.put_item(Item={'Id_Number': 4, 'Value': nameplateEntries})
        s3_client.delete_object(Bucket=bucket, Key=json_file_name)