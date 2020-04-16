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
    recipeIngredient = scrapy.Field()
    recipeInstructions = scrapy.Field()
    recipeYield = scrapy.Field()
    calories = scrapy.Field()
    fat = scrapy.Field()
    protein = scrapy.Field()
    cholesterol = scrapy.Field()
    sodium = scrapy.Field()
    recipeCategory = scrapy.Field()
    aggregateRating = scrapy.Field()
    
    def fields_populated(self):
        populated = True
        for field in self.fields:
            if not field in self.keys():
                populated = False
                break
        return populated
