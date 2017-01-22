import boto3

from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider

from routescraper.dynamodb_wrapper import scan_item
from routescraper.redshift_wrapper import RedshiftWrapper


class CrawlVerifier(object):
    """
    Task is to verify the number of completed queue items in dynamodb
    for the current day and the number of redshift records with today
    as crawl date.

    Another task is to get all failed queue items / or still pending
    queue items and re run the scraper.
    NOTE: Not sure how to handle this. Need to call scrapy crawler
    from here again.
    """
    table_name = 'flightscrapequeue'
    rs = RedshiftWrapper()

    def completed_items_today(self):
        today = datetime.today().strftime("%Y-%m-%d")
        # Count of scraped items in RedShift Database
        rs_item_count = self.rs.get_todays_data_count()
        self.rs.close()

        # Count of completed queue items in DynamoDB
        completed_items = scan_item(
            table_name=self.table_name, status='completed',
            crawl_date=today
        )
        print("Redshift items: {}".format(rs_item_count))
        print("Dynamodb completed items: {}".format(len(completed_items)))
        if rs_item_count != len(completed_items):
            # COUNT MISMATCH
            # SOME ITEMS FAILED
            print("Count Mismatch, some items failed")
            # pending_items = scan_item(
            #     table_name=self.table_name, status='pending',
            #     crawl_date=today
            # )
            # print("Length of failed items: {}".format(len(pending_items)))
            # if len(pending_items):
            #     # format pending items and recrawl them
            #     formatted_records = self.format_records(pending_items)

            #     # call the recrawl method
            #     # self.recrawl_items(formatted_records=formatted_records)

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
                'ToAddresses': [
                    to,
                ],
                # 'CcAddresses': [
                #     'string',
                # ],
                # 'BccAddresses': [
                #     'string',
                # ]
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
                    },
                    # 'Html': {
                    #     'Data': 'string',
                    #     'Charset': 'string'
                    # }
                }
            },
        )
        print(response)


if __name__ == '__main__':
    v = CrawlVerifier()
    v.completed_items_today()
