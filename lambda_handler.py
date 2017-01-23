from abc import ABCMeta, abstractmethod
# import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider

# logger = logging.getLogger()
# logger.setLevel(logging.INFO)


class BaseLambdaHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, item_name):
        pass


class LambdaHandler(BaseLambdaHandler):
    def __init__(self, formatted_records):
        self.formatted_records = formatted_records
        # logger.info('New Data: {}'.format(formatted_records))
        print('New Data: {}'.format(formatted_records))

    # override
    def handle(self):
        process = CrawlerProcess(get_project_settings())
        for site, site_records in self.formatted_records.items():
            if site_records:
                # call each site spider if data exists
                print("Latest code")
                if site == 'airasia':
                    process.crawl(AirAsiaSpider, data=site_records)
                elif site == 'jetstar':
                    process.crawl(JetStarSpider, data=site_records)
                else:
                    pass
        process.start()
        # the script will block here until the crawling is finished
        process.stop()


def lambda_handler(event, context):
    print('Crawal started.')
    records = event.get('Records', [])
    if not records:
        print('No records')
        return False
    else:
        formatted_records = {
            'airasia': [],
            'jetstar': []
        }
        for record in records:
            if record['eventName'] != 'INSERT':
                continue
            queue_data = {
                key: value['S'] for key, value in
                record['dynamodb']['NewImage'].items()
            }
            if queue_data.get('processing_status') != 'completed':
                formatted_records[queue_data['site']].append(queue_data)

        # pass the formatted data to LambdaHandler
        if formatted_records['airasia'] or formatted_records['jetstar']:
            h = LambdaHandler(formatted_records=formatted_records)
            h.handle()
        else:
            print('No records to scrape')
    return True
