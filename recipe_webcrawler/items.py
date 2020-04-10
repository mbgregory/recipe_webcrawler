# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RecipeWebcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    ingredients = scrapy.Field()
    instructions = scrapy.Field()
    servings = scrapy.Field()
    calories = scrapy.Field()
    fat = scrapy.Field()
    protein = scrapy.Field()
    cholesterol = scrapy.Field()
    sodium = scrapy.Field()
    categories = scrapy.Field()
    rating = scrapy.Field()
    review_cnt = scrapy.Field()

    
    def fields_populated(self):
        populated = True
        for field in self.fields:
            if not field in self.keys() and field != 'servings':
                populated = False
                break
        return populated
