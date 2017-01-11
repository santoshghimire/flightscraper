from abc import ABCMeta, abstractmethod
import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class BaseLambdaHandler(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def handle(self, item_name):
        pass


class LambdaHandler(BaseLambdaHandler):
    def __init__(self, data):
        self.data = data
        logger.info('New Data: {0}'.format(data))

    # override
    def handle(self):
        process = CrawlerProcess(get_project_settings())
        try:
            site = self.data['site']
        except:
            raise
        process.crawl(site, data=self.data)
        process.start()
        # the script will block here until the crawling is finished
        process.stop()


def lambda_handler(event, context):
    logger.info('Crawal started.')
    records = event.get('Records', [])
    if not records:
        logger.info('No records')
        return False
    else:
        for record in records:
            if record['eventName'] != 'INSERT':
                continue
            data = {
                key: value['S'] for key, value in record['NewImage'].items()
            }
            if data.get('status') != 'completed':
                h = LambdaHandler(data=data)
                h.handle()
            # update dynamodb
    return True
