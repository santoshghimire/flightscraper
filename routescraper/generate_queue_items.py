from datetime import datetime, timedelta
from dynamodb_wrapper import batch_write, get_today_queue_items_count
import boto3
import time

import logging
logger = logging.getLogger('queueGen')
hdlr = logging.FileHandler('/var/tmp/queueGen.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


def generate():
    """
    Module to generate items for all sites,
    all routes for next 365 days and insert
    to dynamodb queue table.
    """
    table_name = 'flightscrapequeue'
    routes = [
        {"origin": "SIN", "destination": "DPS"},
        {"origin": "SIN", "destination": "BKK"},
        {"origin": "SIN", "destination": "DMK"},
        {"origin": "SIN", "destination": "PER"},
        {"origin": "SIN", "destination": "PEN"},
        {"origin": "SIN", "destination": "HKT"},
        {"origin": "DPS", "destination": "SIN"},
        {"origin": "BKK", "destination": "SIN"},
        {"origin": "DMK", "destination": "SIN"},
        {"origin": "PER", "destination": "SIN"},
        {"origin": "PEN", "destination": "SIN"},
        {"origin": "HKT", "destination": "SIN"}
    ]
    logger.info("Generating scraping queue items for next 365 days ...")
    batch_items = []
    today = datetime.today()
    crawl_date = today.strftime("%Y-%m-%d")
    total_items_count = 0
    for count, site in enumerate(["airasia", "jetstar"]):
        for route in routes:
            logger.info(
                "{0}: {1} to {2}".format(
                    site.title(), route['origin'], route['destination']
                )
            )
            for i in range(1, 366):
                if i > 90 and i <= 180:
                    # 3 to 6 months - scrape every 3 days
                    if i % 3 != 1:
                        continue
                elif i > 180 and i <= 270:
                    # 6 to 9 months - scrape every 5 days
                    if i % 5 != 1:
                        continue
                elif i > 270:
                    # over 9 months - scrape every 7 days
                    if i % 7 != 1:
                        continue
                each_date = today + timedelta(days=i)
                departure_date = each_date.strftime("%Y-%m-%d")
                uuid = '_'.join([
                    crawl_date, site, route['origin'], route['destination'],
                    departure_date
                ])
                item = {
                    'uuid': uuid,
                    'processing_status': 'pending',
                    'origin': route['origin'],
                    'destination': route['destination'],
                    'crawl_date': crawl_date,
                    'departure_date': departure_date,
                    'num_adult': '1',
                    'num_child': '0',
                    'num_infant': '0',
                    'site': site
                }
                if len(batch_items) == 10:
                    batch_write(table_name=table_name, items=batch_items)
                    time.sleep(1)
                    batch_items = []
                batch_items.append(item)
                total_items_count += 1
            time.sleep(1)
            logger.info('ok')
    if batch_items:
        batch_write(table_name=table_name, items=batch_items)
    logger.info("Total items = {}".format(total_items_count))
    prepare_email(table_name)


def prepare_email(table_name):
    # verify the total num of items
    logger.info("Getting count of inserted items.")
    length = get_today_queue_items_count(table_name=table_name)
    logger.info("Inserted items for today: {}".format(length))

    subject = 'DYNAMODB QUEUE ITEM INSERTION STATS'
    receipient = ['santosh.ghimire33@gmail.com', ]
    body = """
Hi Santosh,

Here is the Flight Scrape queue item insertion stats:

Total items inserted = {}
Required = 3648
Missing = {}

Thanks !!
            """.format(length, (3648 - length))
    if length != 3648:
        status = "[ERROR] "
    else:
        status = "[SUCCESS] "
    send_email(
        to=receipient,
        subject=status + subject,
        body=body
    )
    logger.info(status.strip())
    return True


def send_email(to, subject, body):
    client = boto3.client('ses', region_name='us-east-1')
    try:
        response = client.send_email(
            Source='santosh.ghimire33@gmail.com',
            Destination={
                'ToAddresses': to
            },
            Message={
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body,
                        'Charset': 'UTF-8'
                    }
                }
            }
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return True
        else:
            return False
    except:
        return False


def all_queue_items(site='airasia'):
    routes = [
        {"origin": "SIN", "destination": "DPS"},
        {"origin": "SIN", "destination": "BKK"},
        {"origin": "SIN", "destination": "DMK"},
        {"origin": "SIN", "destination": "PER"},
        {"origin": "SIN", "destination": "PEN"},
        {"origin": "SIN", "destination": "HKT"},
        {"origin": "DPS", "destination": "SIN"},
        {"origin": "BKK", "destination": "SIN"},
        {"origin": "DMK", "destination": "SIN"},
        {"origin": "PER", "destination": "SIN"},
        {"origin": "PEN", "destination": "SIN"},
        {"origin": "HKT", "destination": "SIN"}
    ]
    items = []
    today = datetime.today()
    crawl_date = today.strftime("%Y-%m-%d")
    for route in routes:
        for i in range(1, 366):
            each_date = today + timedelta(days=i)
            departure_date = each_date.strftime("%Y-%m-%d")
            uuid = '_'.join([
                crawl_date, site, route['origin'], route['destination'],
                departure_date
            ])
            item = {
                'processing_status': 'pending',
                'origin': route['origin'],
                'destination': route['destination'],
                'crawl_date': crawl_date,
                'departure_date': departure_date,
                'num_adult': '1',
                'num_child': '0',
                'num_infant': '0',
                'site': site,
                'uuid': uuid
            }
            items.append(item)
    return items

if __name__ == '__main__':
    start = datetime.now()
    generate()
    total_seconds = (datetime.now() - start).total_seconds()

    # convert to human readable time
    m, s = divmod(total_seconds, 60)
    h, m = divmod(m, 60)
    natural_time = "%d:%02d:%02d" % (h, m, s)

    logger.info("Total time taken: {} ".format(natural_time))
