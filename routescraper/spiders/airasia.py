# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
from datetime import datetime, timedelta

from routescraper.items import RouteItem


class AirAsiaSpider(scrapy.Spider):
    name = "airasia"
    allowed_domains = ["airasia.com"]

    def __init__(self):
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.origin = 'SIN'
        self.destination = 'DPS'
        self.depart = '2017-01-09'
        self.adult = '1'
        self.child = '0'
        self.infant = '0'
        url = (
            "https://booking.airasia.com/Flight/Select?o1"
            "={0}&d1={1}&culture=en-GB&dd1={2}&ADT={3}&CHD=0"
            "&inl=0&s=true&mon=true&cc=SGD&c=false".format(
                self.origin, self.destination, self.depart, self.adult
            )
        )
        self.start_urls = [url]
        super(AirAsiaSpider, self).__init__()

    def parse(self, response):
        item = RouteItem()

        item['origin'] = self.origin
        item['destination'] = self.destination
        item['num_adult'] = self.adult
        item['num_child'] = self.child
        item['num_infant'] = self.infant
        item['currency'] = 'SGD'
        # body = response.xpath("//body").extract_first()
        # with open('airasia.html', 'wb') as htmlfile:
        #     htmlfile.write(body)

        # get a list of all prices
        prices = response.xpath(
            "//div[@class='avail-fare-price']/text()").extract()
        # convert price to float for finding min price
        price_list = [
            float(i.strip().replace('SGD', '').strip()) for i in prices
        ]
        min_price = min(price_list)
        item['price'] = str(min_price) + ' SGD'
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

        item['departure_date'] = self.depart + ' ' + depart_time

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
        departure_date_obj = datetime.strptime(self.depart, "%Y-%m-%d")
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
        yield item
