# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from redshift_wrapper import RedshiftWrapper
from dynamodb_wrapper import update_item


class RoutescraperPipeline(object):

    def __init__(self):
        self.db = RedshiftWrapper()

    def process_item(self, item, spider):
        # return item
        # Insert data to Redshift table
        self.db.insert_row(dict(item))

        # Update dynamodb queue to show completed status
        update_item(
            table_name='flightscrapequeue',
            item_uuid=item['uuid'],
            new_status='completed'
        )
        return item

    def close_spider(self, spider):
        self.db.close()
