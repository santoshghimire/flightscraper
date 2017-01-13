# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from redshift_wrapper import RedshiftWrapper


class RoutescraperPipeline(object):

    def __init__(self):
        self.db = RedshiftWrapper()

    def process_item(self, item, spider):
        # Insert data to Redshift table
        self.db.insert_row(item)
        return item

    def close_spider(self, spider):
        self.db.close()
