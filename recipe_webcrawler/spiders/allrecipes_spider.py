import scrapy
import re

from scrapy.linkextractors import LinkExtractor
from recipe_webcrawler.spiders.recipe_parser import RecipeParser
from recipe_webcrawler.items import RecipeWebcrawlerItem

class AllRecipesSpider(scrapy.Spider):
    name = 'allrecipes'

    def start_requests(self):
        urls = [
            'https://www.allrecipes.com/recipe/179352/impossibly-easy-cheeseburger-pie',
            'https://www.allrecipes.com/recipe/262060/simple-ground-beef-stroganoff',
            'https://www.allrecipes.com/recipe/228650/easy-white-chicken-chili',
            'https://www.allrecipes.com/recipe/11973/spaghetti-carbonara-ii/',
            'https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/',
            'https://www.allrecipes.com/recipe/54675/roasted-garlic-cauliflower/',
            'https://www.allrecipes.com/recipe/18324/roast-potatoes',
            'https://www.allrecipes.com/recipe/67952/roasted-brussels-sprouts/',
            'https://www.allrecipes.com/recipe/14399/the-best-chicken-salad-ever',
            'https://www.allrecipes.com/recipes/',
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def __get_name(self, response):
        name = response.selector.xpath('//*[@id="recipe-main-content"][@itemprop="name"]/text()').get()
        return name

    def __get_ingredients(self, response):
        ingredients = response.selector.xpath('//*[@itemprop="recipeIngredient"]/text()').getall()
        return ingredients

    def __get_instructions(self, response):
        instructions = response.selector.xpath('//*[@class="recipe-directions__list--item"]/text()').getall()
        if instructions:
            instructions = ' '.join(instructions)
            instructions = re.sub(r'\s+',' ', instructions)
        return instructions 

    def __get_calories(self, response):
        calorie = None
        calorie_str = response.selector.xpath('//*[@itemprop="calories"]/text()').get()
        if calorie_str:
            calorie = calorie_str.split()[0]
            calorie = float(calorie)
        return calorie 

    def __get_fat(self, response):
        fat = None
        fat_str = response.selector.xpath('//*[@itemprop="fatContent"]/text()').get()
        if fat_str:
            fat = fat_str.strip()
            fat = float(fat)
        return fat 

    def __get_protein(self, response):
        protein = None
        protein_str = response.selector.xpath('//*[@itemprop="proteinContent"]/text()').get()
        if protein_str:
            protein = protein_str.strip()
            protein = float(protein)
        return protein 

    def __get_cholesterol(self, response):
        cholesterol_re = re.compile(r'<\s1\s')
        cholesterol = None
        cholesterol_str = response.selector.xpath('//*[@itemprop="cholesterolContent"]/text()').get()
        if cholesterol_str:
            m = cholesterol_re.match(cholesterol_str)
            if m:
                cholesterol_str = '1' 
        if cholesterol_str:
            cholesterol = cholesterol_str.strip()
            cholesterol = float(cholesterol)
        return cholesterol 

    def __get_sodium(self, response):
        sodium = None
        sodium_str = response.selector.xpath('//*[@itemprop="sodiumContent"]/text()').get()
        if sodium_str:
            sodium = sodium_str.strip()
            sodium = float(sodium)
        return sodium 

    def __get_servings(self, response):
        servings = None
        servings = response.selector.xpath('//*[@itemprop="recipeYield"]/@content').get()
        try: 
            servings = float(servings)
        except ValueError:
            servings = None 
        return servings

    def __get_categories(self, response):
        categories = None
        categories = response.selector.xpath('//*[@itemprop="recipeCategory"]/@content').getall()
        return categories

    def __get_rating(self, response):
        rating = None
        rating_scale = None
        rating_str = response.selector.xpath('//*[@property="og:rating"]/@content').get()
        rating_scale_str = response.selector.xpath('//*[@property="og:rating_scale"]/@content').get()
        if rating_str:
            rating = float(rating_str)
        if rating_scale_str:
            rating_scale = float(rating_scale_str)
        return {'value':rating, 'scale':rating_scale}

    def __get_review_cnt(self, response):
        review_re = re.compile(r'(?P<count>\d+)k')
        review_cnt = None
        review_cnt_str = response.selector.xpath('//*[@class="review-count"]/text()').get()
        if review_cnt_str:
            m = review_re.match(review_cnt_str)
            if m:
                review_cnt = int(m.group('count')) * 1000
            else:
                review_cnt = int(review_cnt_str.split()[0])
        return review_cnt 
    
    def __get_recipe_json(self, response):
        json_str = response.selector.xpath('//*[@type="application/ld+json"]/text()').get()
        return json_str

    def parse(self, response):
        recipe_item = RecipeWebcrawlerItem() 
        recipe_item['url'] = response.url

        json_str = self.__get_recipe_json(response)
        if json_str is not None:
            rp = RecipeParser(json_str)
            if rp.completed():                 
                recipe_item['name'] = rp.get_recipe_name()
                recipe_item['ingredients'] = rp.get_recipe_ingredient()
                recipe_item['instructions'] = rp.get_recipe_instructions()
                nutrition = rp.get_nutrition()
                recipe_item['calories'] = nutrition['calories']['quantity']
                recipe_item['fat'] = nutrition['fatContent']['quantity']
                recipe_item['protein'] = nutrition['proteinContent']['quantity']
                recipe_item['cholesterol'] = nutrition['cholesterolContent']['quantity']
                recipe_item['sodium'] = nutrition['sodiumContent']['quantity']
                recipe_item['categories'] = rp.get_recipe_category()
                recipe_item['rating'] = rp.get_rating()
                recipe_item['review_cnt'] = rp.get_review_cnt()
        else:
            recipe_item['name'] = self.__get_name(response)
            recipe_item['ingredients'] = self.__get_ingredients(response)
            recipe_item['instructions'] = self.__get_instructions(response)
            recipe_item['servings'] = self.__get_servings(response)
            recipe_item['calories'] = self.__get_calories(response)
            recipe_item['fat'] = self.__get_fat(response)
            recipe_item['protein'] = self.__get_protein(response)
            recipe_item['cholesterol'] = self.__get_cholesterol(response)
            recipe_item['sodium'] = self.__get_sodium(response)
            recipe_item['categories'] = self.__get_categories(response)
            recipe_item['rating'] = self.__get_rating(response)
            recipe_item['review_cnt'] = self.__get_review_cnt(response)

        if recipe_item.fields_populated():
            yield recipe_item

        allow_re = ['https://www.allrecipes\.com/recipe.*']
        deny_re = ['https://www.allrecipes\.com/recipe/\d+/.*/reviews/.*','https://www.allrecipes\.com/recipe/\d+/.*/photos/.*']
        links = LinkExtractor(allow=allow_re, deny=deny_re, allow_domains=['allrecipes.com'], unique=True).extract_links(response)
        for link in links:
            if link is not None:
                yield response.follow(link, callback=self.parse)

