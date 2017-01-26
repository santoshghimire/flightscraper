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


def scan_item(table_name, status, crawl_date):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    response = table.scan(
        FilterExpression=Attr('processing_status').eq(status) &
        Attr('crawl_date').eq(crawl_date)
    )
    items = response['Items']
    return items


def delete_item(table_name, uuid):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    response = table.delete_item(
        Key={'uuid': uuid}
    )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False


def create_table(table_name):
    # Create the DynamoDB table.
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'uuid',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uuid',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
    return table


def delete_all_items(table_name):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
    table = dynamodb.Table(table_name)
    table.delete()
    table = create_table(table_name)
    if table:
        print("Success !!")


if __name__ == '__main__':
    table_name = 'flightscrapequeue'
    # # # 1. Create
    # item = {
    #     'processing_status': 'pending',
    #     'origin': 'SIN',
    #     'destination': 'DPS',
    #     'crawl_date': '2017-01-23',
    #     'departure_date': '2017-01-24',
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
    # items = [
    #     {
    #         'processing_status': 'pending',
    #         'origin': 'SIN',
    #         'destination': 'DPS',
    #         'crawl_date': '2017-01-16',
    #         'departure_date': '2017-01-18',
    #         'num_adult': '1',
    #         'num_child': '0',
    #         'num_infant': '0',
    #         'site': 'airasia'
    #     },
    #     {
    #         'processing_status': 'pending',
    #         'origin': 'SIN',
    #         'destination': 'DPS',
    #         'crawl_date': '2017-01-16',
    #         'departure_date': '2017-01-18',
    #         'num_adult': '1',
    #         'num_child': '0',
    #         'num_infant': '0',
    #         'site': 'jetstar'
    #     }
    # ]
    # status = batch_write(table_name=table_name, items=items)
    # print(status)
    # uuid_string = "e591334f-5384-4794-a76d-f58a1bb14d3c"
    # status = delete_item(
    #     table_name=table_name,
    #     uuid=uuid_string
    # )
    # print(status)
    delete_all_items(table_name=table_name)
    create_table(table_name)
