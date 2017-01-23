# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RouteItem(scrapy.Item):
    # define the fields for your item here like:
    uuid = scrapy.Field()
    airline_name = scrapy.Field()
    origin = scrapy.Field()
    destination = scrapy.Field()
    num_adult = scrapy.Field()
    num_child = scrapy.Field()
    num_infant = scrapy.Field()
    flight_number = scrapy.Field()
    fare_class = scrapy.Field()
    departure_date = scrapy.Field()
    arrival_date = scrapy.Field()
    price_date = scrapy.Field()
    price = scrapy.Field()
    days_to_flight = scrapy.Field()
    currency = scrapy.Field()
    site = scrapy.Field()
