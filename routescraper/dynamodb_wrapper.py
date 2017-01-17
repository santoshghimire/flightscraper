import boto3
import uuid
from boto3.dynamodb.conditions import Attr


def batch_write(table_name, items):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    with table.batch_writer() as batch:
        for item in items:
            item['uuid'] = str(uuid.uuid4())
            batch.put_item(Item=item)
    return True


def insert_item(table_name, item):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)

    item['uuid'] = str(uuid.uuid4())
    response = table.put_item(Item=item)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def get_item(table_name, query_item):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    response = table.get_item(
        Key=query_item
    )
    item = response['Item']
    return item


def update_item(table_name, item_uuid, new_status):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={"uuid": item_uuid},
        UpdateExpression='SET processing_status = :val1',
        ExpressionAttributeValues={
            ':val1': new_status
        }
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def scan_item(table_name, status):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=Attr('processing_status').eq(status)
    )
    items = response['Items']
    return items


if __name__ == '__main__':
    table_name = 'flightscrapequeue'
    # # # 1. Create
    # item = {
    #     'processing_status': 'pending',
    #     'origin': 'SIN',
    #     'destination': 'DPS',
    #     'crawl_date': '2017-01-13',
    #     'departure_date': '2017-01-15',
    #     'num_adult': '1',
    #     'num_child': '0',
    #     'num_infant': '0',
    #     'site': 'airasia'
    #     # 'site': 'jetstar'
    # }
    # status = insert_item(table_name=table_name, item=item)
    # print(status)
    # # 2. scan
    # items = scan_item(table_name=table_name, status='pending')
    # print(len(items))
    # # 3. Update
    # response = update_item(
    #     table_name=table_name, item_uuid=items[0]['uuid'],
    #     new_status="completed"
    # )
    # print(response)
    # 4. Batch write
    items = [
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-16',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'airasia'
        },
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-16',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'jetstar'
        }
    ]
    status = batch_write(table_name=table_name, items=items)
    print(status)
