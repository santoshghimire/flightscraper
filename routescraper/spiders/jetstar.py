# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
import uuid
from datetime import datetime, timedelta

from routescraper.items import RouteItem


class JetStarSpider(scrapy.Spider):
    name = "jetstar"
    allowed_domains = ["jetstar.com"]
    start_urls = ['http://www.jetstar.com/sg/en/home']

    def __init__(self, data=None):
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if not data:
            today = datetime.today()
            depart_obj = today + timedelta(days=2)
            depart_date = depart_obj.strftime("%Y-%m-%d")
            data = [{
                'processing_status': 'pending',
                'origin': 'SIN',
                'destination': 'DPS',
                'crawl_date': today.strftime("%Y-%m-%d"),
                'departure_date': depart_date,
                'num_adult': '1',
                'num_child': '0',
                'num_infant': '0',
                'site': 'jetstar',
                'uuid': str(uuid.uuid4())
            }]
            print('From cmd, using dummy input data', data)
        self.data = data
        super(JetStarSpider, self).__init__()

    def parse(self, response):
        for record in self.data:
            url = (
                "https://booking.jetstar.com/sg/en/booking/search-flights"
                "?origin1={0}&destination1={1}&departuredate1={2}"
                "&adults={3}&children={4}&infants={5}&currency=SGD"
                "&uuid={6}".format(
                    record['origin'], record['destination'],
                    record['departure_date'], record['num_adult'],
                    record['num_child'], record['num_infant'],
                    record['uuid']
                )
            )
            yield scrapy.Request(
                url, callback=self.parse_results,
                meta=record
            )

    def parse_results(self, response):
        item = RouteItem()

        item['origin'] = response.meta['origin']
        item['destination'] = response.meta['destination']
        item['num_adult'] = response.meta['num_adult']
        item['num_child'] = response.meta['num_child']
        item['num_infant'] = response.meta['num_infant']
        depart = response.meta['departure_date']
        item['uuid'] = response.meta['uuid']

        elem = response.xpath(
            "//div[contains(@class, 'fare-row js-fare-row')]"
        )
        elem = elem[0]
        depart_time = elem.xpath(
            ".//div[@class="
            "'columns fare__departure-time js-departure-time departuretime'"
            "]/text()"
        ).extract_first().strip()
        am_pm = elem.xpath(
            ".//div[@class="
            "'columns fare__departure-time js-departure-time departuretime'"
            "]/span/text()"
        ).extract_first().strip()
        full_depart_datetime = depart + ' ' + depart_time +\
            ' ' + am_pm.upper()
        depart_date_obj = datetime.strptime(
            full_depart_datetime, "%Y-%m-%d %I:%M %p")
        item['departure_date'] = depart_date_obj.strftime('%Y-%m-%d %H:%M')
        item['days_to_flight'] = (depart_date_obj - datetime.today()).days
        price = elem.xpath(
            ".//span[@class='price js-price']/text()"
        ).extract_first().strip()
        item['price'] = float(price)
        item['price_date'] = datetime.now().strftime('%Y-%m-%d')
        item['currency'] = elem.xpath(
            ".//span[@class='currency-symbol']/text()"
        ).extract_first().strip()

        item['flight_number'] = elem.xpath(
            ".//div[@class='row fare__info-flight-number']"
            "/div[@class='medium-11 columns']/strong/text()"
        ).extract_first().strip()

        arrival_date = elem.xpath(
            ".//strong[@class='arrivalstation']/text()"
        ).extract_first().strip()
        arrival_date = arrival_date.replace(',', '')
        arrival_date_obj = datetime.strptime(
            arrival_date, "%I:%M%p %A %d %B %Y")
        item['arrival_date'] = arrival_date_obj.strftime('%Y-%m-%d %H:%M')

        item['fare_class'] = elem.xpath(
            ".//strong[@class='cabintype']/text()"
        ).extract_first().strip()
        item['airline_name'] = elem.xpath(
            ".//strong[@class='operatedby']/text()"
        ).extract_first().strip()

        yield item
