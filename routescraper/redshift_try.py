import boto3

client = boto3.client('redshift', region_name='us-east-1')
print(client)
