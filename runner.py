from datetime import datetime
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider
from routescraper.dynamodb_wrapper import query_item


def main(site='both'):
    """
    Query items in dynamodb and start scrape.
    """
    table_name = 'flightscrapequeue'
    today_pending_items = query_item(
        table_name=table_name,
        status='pending',
        crawl_date=datetime.today().strftime("%Y-%m-%d")
    )
    # Debugging on
    # print(len(today_pending_items))
    # today_pending_items = today_pending_items[:20]
    # from pprint import pprint
    # pprint(today_pending_items)
    # Debugging off
    # return
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


def is_odd(num):
    if num % (num / 2):
        return True
    else:
        return False

if __name__ == '__main__':
    # sites = ['airasia', 'jetstar']
    # today = datetime.today().day
    # if is_odd(today):
    #     main(site=sites[0])
    # else:
    #     main(site=sites[1])
    main(site="both")
