from datetime import datetime, timedelta
from dynamodb_wrapper import batch_write
import time


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
    for route in routes:
        today = datetime.today()
        for site in ["airasia", "jetstar"]:
            items = []
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
            time.sleep(1)
    return True

if __name__ == '__main__':
    generate()
