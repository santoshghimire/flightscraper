from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider
from routescraper.dynamodb_wrapper import scan_item


def main():
    """
    Scan items in dynamodb and start scrape.
    """
    table_name = 'flightscrapequeue'
    today_pending_items = scan_item(
        table_name=table_name,
        status='pending',
        crawl_date=datetime.today().strftime("%Y-%m-%d")
    )
    items = {
        'airasia': [], 'jetstar': []
    }
    for item in today_pending_items:
        if item.get('site') == 'airasia':
            items['airasia'].append(item)
        elif item.get('site') == 'jetstar':
            items['jetstar'].append(item)
        else:
            print("Unknown site {}".format(item['site']))

    process = CrawlerProcess(get_project_settings())
    for site, site_records in items.items():
        if site == 'airasia':
            process.crawl(AirAsiaSpider, data=site_records)
        elif site == 'jetstar':
            process.crawl(JetStarSpider, data=site_records)
        else:
            pass
    process.start()
    # the script will block here until the crawling is finished
    process.stop()

if __name__ == '__main__':
    main()
