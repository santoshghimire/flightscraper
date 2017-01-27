from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider
from routescraper.dynamodb_wrapper import scan_item


def main(site='both'):
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
        if (
            item.get('site') == 'airasia' and
            (site == 'both' or site == 'airasia')
        ):
            items['airasia'].append(item)
        elif (
            item.get('site') == 'jetstar' and
            (site == 'both' or site == 'jetstar')
        ):
            items['jetstar'].append(item)
        else:
            pass
    if items['airasia'] or items['jetstar']:
        process = CrawlerProcess(get_project_settings())
    for site, site_records in items.items():
        if site == 'airasia' and site_records:
            process.crawl(AirAsiaSpider, data=site_records)
        elif site == 'jetstar' and site_records:
            process.crawl(JetStarSpider, data=site_records)
        else:
            pass
    process.start()
    # the script will block here until the crawling is finished
    process.stop()

if __name__ == '__main__':
    main()
    # main(site='airasia')
    # main(site='jetstar')
