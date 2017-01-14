# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
# import json
import urlparse
import uuid
from datetime import datetime, timedelta

from routescraper.items import RouteItem


class AirAsiaSpider(scrapy.Spider):
    name = "airasia"
    allowed_domains = ["airasia.com"]
    start_urls = []

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
                'site': 'airasia',
                'uuid': str(uuid.uuid4())
            }]
            print('From cmd, using dummy input data', data)
        for record in data:
            url = (
                "https://booking.airasia.com/Flight/Select?o1"
                "={0}&d1={1}&culture=en-GB&dd1={2}&ADT={3}&CHD=0"
                "&inl=0&s=true&mon=true&cc=SGD&c=false&uuid={4}".format(
                    record['origin'], record['destination'],
                    record['departure_date'], record['num_adult'],
                    record['uuid']
                )
            )
            self.start_urls.append(url)
        super(AirAsiaSpider, self).__init__()

    def parse(self, response):
        item = RouteItem()
        params = urlparse.parse_qs(response.url)
        item['origin'] = params[
            'https://booking.airasia.com/Flight/Select?o1'][0]
        item['destination'] = params['d1'][0]
        item['num_adult'] = params['ADT'][0]
        item['num_child'] = params['CHD'][0]
        item['num_infant'] = params['inl'][0]
        item['currency'] = params['cc'][0]
        depart = params['dd1'][0]
        item['uuid'] = params['uuid'][0]

        # get a list of all prices
        prices = response.xpath(
            "//div[@class='avail-fare-price']/text()").extract()
        # convert price to float for finding min price
        price_list = [
            float(i.strip().replace('SGD', '').strip()) for i in prices
        ]
        min_price = min(price_list)
        item['price'] = min_price
        actual_min_price = prices[price_list.index(min_price)]

        # find actual min flight element
        detail_elem = response.xpath(
            "//div[@class='avail-fare-price'][contains(text(),'" +
            actual_min_price + "')]" +
            "/ancestor::tr[@class='fare-dark-row']"
        )
        # departure time
        depart_time = detail_elem.xpath(
            ".//tr[@class='fare-dark-row']/td[@class='avail-table-detail']"
        )[0].xpath(".//div[@class='avail-table-bold']/text()").extract_first()

        item['departure_date'] = depart + ' ' + depart_time

        # arrival time
        arrive_time = detail_elem.xpath(
            ".//tr[@class='fare-dark-row']/td[@class='avail-table-detail']"
        )[1].xpath(".//div[@class='avail-table-bold']/text()").extract_first()

        # arrival day
        arrive_day = detail_elem.xpath(
            ".//tr[@class='fare-dark-row']/td[@class='avail-table-detail']"
        )[1].xpath(
            ".//div[@class='avail-table-next-day']/text()"
        ).extract_first()
        departure_date_obj = datetime.strptime(depart, "%Y-%m-%d")
        arrival_date_obj = departure_date_obj
        if arrive_day == '+1':
            arrival_date_obj = departure_date_obj + timedelta(1)
        item['arrival_date'] = arrival_date_obj.strftime("%Y-%m-%d") + ' ' +\
            arrive_time

        item['price_date'] = datetime.now().strftime('%Y-%m-%d')
        item['days_to_flight'] = (departure_date_obj - datetime.today()).days

        flight_num = detail_elem.xpath(
            ".//div[@class='carrier-hover-bold']/text()").extract_first()
        item['flight_number'] = flight_num
        career_symbol = flight_num[:2]
        carriers = response.xpath(
            "//span[@class='carrier-legend-desc']/text()").extract()
        carriers = [i.strip() for i in carriers]
        airline_name = [
            i for i in carriers if i.startswith(career_symbol + ' -')]
        if airline_name:
            item['airline_name'] = airline_name[0]
        else:
            item['airline_name'] = ''
        item['fare_class'] = ''
        yield item
