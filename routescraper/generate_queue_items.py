from datetime import datetime, timedelta
from dynamodb_wrapper import batch_write
import uuid
# import time

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
    for count, site in enumerate(["airasia", "jetstar"]):
        for route in routes:
            today = datetime.today()
            items = []
            logger.info(
                "{0}: {1} to {2}".format(
                    site.title(), route['origin'], route['destination']
                )
            )
            for i in range(1, 366):
                each_date = today + timedelta(days=i)
                departure_date = each_date.strftime("%Y-%m-%d")
                item = {
                    'processing_status': 'pending',
                    'origin': route['origin'],
                    'destination': route['destination'],
                    'crawl_date': today.strftime("%Y-%m-%d"),
                    'departure_date': departure_date,
                    'num_adult': '1',
                    'num_child': '0',
                    'num_infant': '0',
                    'site': site
                }
                items.append(item)
            # batch write
            batch_write(table_name=table_name, items=items)
            logger.info('ok')
            # time.sleep(10)
    return True


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
    for route in routes:
        today = datetime.today()
        for i in range(1, 366):
            each_date = today + timedelta(days=i)
            departure_date = each_date.strftime("%Y-%m-%d")
            item = {
                'processing_status': 'pending',
                'origin': route['origin'],
                'destination': route['destination'],
                'crawl_date': today.strftime("%Y-%m-%d"),
                'departure_date': departure_date,
                'num_adult': '1',
                'num_child': '0',
                'num_infant': '0',
                'site': site,
                'uuid': str(uuid.uuid4())
            }
            items.append(item)
    return items

if __name__ == '__main__':
    generate()
    # all_queue_items()
