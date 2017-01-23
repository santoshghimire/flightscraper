from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from routescraper.spiders.airasia import AirAsiaSpider
from routescraper.spiders.jetstar import JetStarSpider

items = {
    "airasia": [
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-22',
            'departure_date': '2017-01-23',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'airasia',
            'uuid': 'ded71d0f-899b-4975-90f2-34cb19b2f2e7'
        }
    ],
    "jetstar": [
        {
            'processing_status': 'pending',
            'origin': 'SIN',
            'destination': 'DPS',
            'crawl_date': '2017-01-22',
            'departure_date': '2017-01-23',
            'num_adult': '1',
            'num_child': '0',
            'num_infant': '0',
            'site': 'jetstar',
            'uuid': '9c74160a-741e-4659-8a84-b7d49eb63708'
        }
    ]
}

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
