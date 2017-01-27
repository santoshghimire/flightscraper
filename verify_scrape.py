import boto3

from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider

from routescraper.dynamodb_wrapper import (
    scan_item, get_today_queue_items_count
)
from routescraper.redshift_wrapper import RedshiftWrapper

import logging
logger = logging.getLogger('queueGen')
hdlr = logging.FileHandler('/var/tmp/verifyScrape.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class CrawlVerifier(object):
    """
    Task is to verify the number of completed queue items in dynamodb
    for the current day and the number of redshift records with today
    as crawl date.

    Another task is to get all failed queue items / or still pending
    queue items and re run the scraper.
    """
    table_name = 'flightscrapequeue'
    rs = RedshiftWrapper()

    # Email default params
    receipients = ['hiteshsc@gmail.com', 'santosh.ghimire33@gmail.com', ]

    def completed_items_today(self):
        today = datetime.today().strftime("%Y-%m-%d")
        subject = "Scraper Report for {}".format(today)
        today_count = get_today_queue_items_count(self.table_name)

        # Construct Email body
        body = (
            "Here is the stats for Flightinfo scrape "
            "of Airasia and Jetstar for {}:\n\n".format(today)
        )
        today_count_msg = "Items to be scraped today: {}\n".format(today_count)
        body += today_count_msg
        logger.info(today_count_msg)

        # Count of scraped items in RedShift Database
        rs_item_count = self.rs.get_todays_data_count()
        self.rs.close()
        redshift_msg = "Flightinfo Items in Redshift: {}\n".format(
            rs_item_count)
        body += redshift_msg
        logger.info(redshift_msg)

        # Count of completed queue items in DynamoDB
        completed_items = scan_item(
            table_name=self.table_name, status='completed',
            crawl_date=today
        )
        dynamo_complete_msg = "Completed queue items in Dynamodb: {}\n".format(
            len(completed_items))
        body += dynamo_complete_msg
        logger.info(dynamo_complete_msg)

        pending_items_len = 0
        # Both Should be equal to 8760
        if rs_item_count != len(completed_items):
            # COUNT MISMATCH
            # SOME ITEMS FAILED
            mismatch_msg = "Count Mismatch, some items are pending/failed\n"
            body += mismatch_msg
            logger.info(mismatch_msg)
            pending_items = scan_item(
                table_name=self.table_name, status='pending',
                crawl_date=today
            )
            pending_items_len = len(pending_items)

        pending_msg = "Total pending/failed items: {}".format(
            pending_items_len)
        body += pending_msg
        logger.info(pending_msg)

        if pending_items_len:
            recrawl_msg = (
                "Recrawl started for {} pending/failed items\n".format(
                    pending_items_len
                )
            )
            body += recrawl_msg
            logger.info(recrawl_msg)

        body += "\n\nThanks !!"
        status = self.send_email(
            to=self.receipients,
            subject=subject,
            body=body
        )
        if status:
            logger.info("Email Sent")
        else:
            logger.info("Error in sending email")
        # UNCOMMENT THE FOLLOWING TO ALLOW RECRAWL OF PENDING/FAILED ITEMS
        if pending_items_len:
            # format pending items and recrawl them
            formatted_records = self.format_records(pending_items)

            # call the recrawl method
            self.recrawl_items(formatted_records=formatted_records)

    def format_records(self, pending_items):
        formatted_records = {
            'airasia': [],
            'jetstar': []
        }
        for record in pending_items:
            formatted_records[record['site']].append(record)
        return formatted_records

    def recrawl_items(self, formatted_records):
        process = CrawlerProcess(get_project_settings())
        for site, site_records in formatted_records.items():
            if site_records:
                # call each site spider if data exists
                if site == 'airasia':
                    process.crawl(AirAsiaSpider, data=site_records)
                elif site == 'jetstar':
                    process.crawl(JetStarSpider, data=site_records)
                else:
                    pass
        process.start()
        # the script will block here until the crawling is finished
        process.stop()

    def send_email(self, to, subject, body):
        client = boto3.client('ses', region_name='us-east-1')
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

    def send_demo_email(self):
        today = datetime.today().strftime("%Y-%m-%d")
        subject = "Scraper Report for {}".format(today)

        # fake stats
        today_count = 8760
        rs_item_count = 8760
        completed_items = 8760
        pending_items_len = 0

        body = (
            "Here is the stats for Flightinfo scrape "
            "for Airasia and Jetstar for {}:\n\n".format(today)
        )
        today_count_msg = "Items to be scraped today: {}\n".format(today_count)
        body += today_count_msg

        redshift_msg = "Flightinfo Items in Redshift: {}\n".format(
            rs_item_count)
        body += redshift_msg

        dynamo_complete_msg = "Completed queue items in Dynamodb: {}\n".format(
            completed_items)
        body += dynamo_complete_msg

        pending_msg = "Total pending/failed items: {}".format(
            pending_items_len)
        body += pending_msg
        body += "\n\nThanks !!"
        self.send_email(
            to=['santosh.ghimire33@gmail.com'],
            subject=subject,
            body=body
        )


if __name__ == '__main__':
    v = CrawlVerifier()
    v.completed_items_today()
    # v.send_demo_email()
