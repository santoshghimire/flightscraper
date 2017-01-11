# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class RoutescraperPipeline(object):
    def process_item(self, item, spider):
        # USE BOTO3 to save item to Redshift
        # Create a table in redshift to store the items.
        # and insert row in the table.
        return item
