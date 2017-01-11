# -*- coding: utf-8 -*-
import scrapy
import sys
import codecs
import locale
import json
from datetime import datetime

from routescraper.items import RouteItem


class JetStarSpider(scrapy.Spider):
    name = "jetstar"
    allowed_domains = ["jetstar.com"]

    def __init__(self, data):
        if type(data) == str:
            try:
                data = json.loads(data)
            except:
                raise
        sys.stdout = codecs.getwriter(
            locale.getpreferredencoding())(sys.stdout)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.origin = data.get('origin', 'SIN')
        self.destination = data.get('destination', 'DPS')
        self.depart = data('departure_date', '2017-01-12')
        self.adult = data.get('num_adult', '1')
        self.child = data.get('num_child', '0')
        self.infant = data.get('num_infant', '0')
        url = (
            "https://booking.jetstar.com/sg/en/booking/search-flights"
            "?origin1={0}&destination1={1}&departuredate1={2}"
            "&adults={3}&children={4}&infants={5}&currency=SGD".format(
                self.origin, self.destination, self.depart, self.adult,
                self.child, self.infant
            )
        )
        self.start_urls = [url]
        super(JetStarSpider, self).__init__()

    def parse(self, response):
        item = RouteItem()

        item['origin'] = self.origin
        item['destination'] = self.destination
        item['num_adult'] = self.adult
        item['num_child'] = self.child
        item['num_infant'] = self.infant

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
        full_depart_datetime = self.depart + ' ' + depart_time +\
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
