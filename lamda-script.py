import json
import boto3
import os

s3_client = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

REPLICA_BUCKET = os.environ['REPLICA_BUCKET']
DYNAMODB_TABLE = os.environ['DYNAMODB_TABLE']

def lambda_handler(event, context):
    # Get the bucket and object key from the S3 event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Copy the object to the replica bucket
    copy_source = {'Bucket': source_bucket, 'Key': object_key}
    s3_client.copy_object(CopySource=copy_source, Bucket=REPLICA_BUCKET, Key=object_key)
    
    # Log information in DynamoDB
    table = dynamodb.Table(DYNAMODB_TABLE)
    table.put_item(Item={
        'Name': object_key,
        'SourceBucket': source_bucket,
        'ReplicaBucket': REPLICA_BUCKET,
        'Timestamp': str(event['Records'][0]['eventTime'])
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps('File replicated and metadata logged successfully')
    }
