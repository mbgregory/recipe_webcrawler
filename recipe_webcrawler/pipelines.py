# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import hashlib

from elasticsearch import Elasticsearch
from recipe_webcrawler.items import RecipeWebcrawlerItem


class RecipeWebcrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class ElasticsearchPipeline(object):

    index_settings = {
        'settings': {
            'number_of_shards':1,
            'number_of_replicas':0,
        }
    }

    def __init__(self):
        self._index_name = 'recipes'
        self._doc_type = 'recipe'

    def open_spider(self, spider):
        self._es  = Elasticsearch()
        if not self._es.indices.exists(index=self._index_name):
            self._es.indices.create(index=self._index_name, body=self.index_settings)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self._es.index(id=hashlib.sha256(str(item['url']).encode()).hexdigest(), 
                       index=self._index_name, 
                       doc_type=self._doc_type, 
                       body=dict(item))
        return item
