from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

items = {
    "airasia": [
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-17',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'airasia',
            'uuid': 'ded71d0f-899b-4975-90f2-34cb19b2f2e7'
        },
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-17',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'airasia',
            'uuid': 'd4817589-f204-4f02-95ac-0ee1063af444'
        }
    ],
    "jetstar": [
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-17',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'jetstar',
            'uuid': '9c74160a-741e-4659-8a84-b7d49eb63708'
        },
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-17',
            'departure_date': '2017-01-18',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'jetstar',
            'uuid': '0e2e98b4-3191-4265-a4f9-83458b1fb781'
        }
    ]
}

for site, records in items.items():
    process = CrawlerProcess(get_project_settings())
    process.crawl(site, data=records)
    process.start()
    # the script will block here until the crawling is finished
    process.stop()
