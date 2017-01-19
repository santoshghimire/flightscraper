from datetime import datetime

from dynamodb_wrapper import scan_item


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

    def completed_items_today(self):
        today = datetime.today().strftime("%Y-%m-%d")
        completed_items = scan_item(
            table_name=self.table_name, status='completed',
            crawl_date=today
        )
        pending_items = scan_item(
            table_name=self.table_name, status='pending',
            crawl_date=today
        )
        print("Length of today completed items: {}".format(
            len(completed_items)))
        print("Length of today pending items: {}".format(
            len(pending_items)))

    def scraped_items_today(self):
        """
        Get count of today's scraped items in redshift.
        """
        pass

if __name__ == '__main__':
    v = CrawlVerifier()
    v.completed_items_today()
