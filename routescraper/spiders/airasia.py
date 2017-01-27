# -*- coding: utf-8 -*-
import scrapy
import re
import sys
import codecs
import locale
from datetime import datetime, timedelta

from routescraper.items import RouteItem
from routescraper.generate_queue_items import all_queue_items


class AirAsiaSpider(scrapy.Spider):
    name = "airasia"
    allowed_domains = ["airasia.com"]
    start_urls = ["http://www.airasia.com/ot/en/home.page?cid=1"]

    def __init__(self, data=None):
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        if not data:
            data = all_queue_items('airasia')
        self.data = data
        super(AirAsiaSpider, self).__init__()

    def parse(self, response):
        for record in self.data:
            url = (
                "https://booking.airasia.com/Flight/Select?o1"
                "={0}&d1={1}&culture=en-GB&dd1={2}&ADT={3}&CHD=0"
                "&inl=0&s=true&mon=true&cc=SGD&c=false&uuid={4}".format(
                    record['origin'], record['destination'],
                    record['departure_date'], record['num_adult'],
                    record['uuid']
                )
            )
            yield scrapy.Request(
                url, callback=self.parse_results,
                meta=record, dont_filter=True
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
        item['site'] = 'jetstar'
        item['currency'] = "SGD"

        # get a list of all prices
        prices = response.xpath(
            "//div[@class='avail-fare-price']/text()").extract()
        # convert price to float for finding min price
        price_list = []
        for p in prices:
            price = re.findall("\d+\.\d+", p)
            price_list.extend([float(i) for i in price])
        try:
            min_price = min(price_list)
        except:
            self.logger.info('Flightinfo not available for {}'.format(depart))
            min_price = None
        if min_price is not None:
            item['price'] = min_price
            actual_min_price = prices[price_list.index(min_price)]

            # find actual min flight element
            detail_elem = response.xpath(
                "//div[@class='avail-fare-price'][contains(text(),'" +
                actual_min_price + "')]" +
                "/ancestor::tr[@class='fare-dark-row']"
            )
            fare_elem = 'fare-dark-row'
            if not detail_elem:
                detail_elem = response.xpath(
                    "//div[@class='avail-fare-price'][contains(text(),'" +
                    actual_min_price + "')]" +
                    "/ancestor::tr[@class='fare-light-row']"
                )
                fare_elem = 'fare-light-row'

            # departure time
            depart_time_elem = detail_elem.xpath(
                ".//tr[@class='" + fare_elem + "']/td"
                "[@class='avail-table-detail']"
            )
            if depart_time_elem:
                depart_time = depart_time_elem[0].xpath(
                    ".//div[@class='avail-table-bold']/text()").extract_first()
            else:
                depart_time = ''
            item['departure_date'] = depart + ' ' + depart_time

            # arrival time
            arrive_time_elem = detail_elem.xpath(
                ".//tr[@class='" + fare_elem + "']/td"
                "[@class='avail-table-detail']"
            )
            if arrive_time_elem:
                arrive_time = arrive_time_elem[1].xpath(
                    ".//div[@class='avail-table-bold']/text()"
                ).extract_first()
            else:
                arrive_time = ''
            # arrival day
            arrive_day = detail_elem.xpath(
                ".//tr[@class='" + fare_elem +
                "']/td[@class='avail-table-detail']"
            )[1].xpath(
                ".//div[@class='avail-table-next-day']/text()"
            ).extract_first()
            departure_date_obj = datetime.strptime(depart, "%Y-%m-%d")
            arrival_date_obj = departure_date_obj
            if arrive_day == '+1':
                arrival_date_obj = departure_date_obj + timedelta(1)
            item['arrival_date'] = arrival_date_obj.strftime("%Y-%m-%d") +\
                ' ' + arrive_time

            item['price_date'] = datetime.now().strftime('%Y-%m-%d')
            item['days_to_flight'] = (
                departure_date_obj - datetime.today()).days

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
