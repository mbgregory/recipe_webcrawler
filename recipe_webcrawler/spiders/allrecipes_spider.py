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
        return {'ratingValue':rating, 'bestRating':rating_scale}

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
   
    def __get_recipe_yield(self, response):
        recipe_yield_re = re.compile(r'\s*Servings Per Recipe:\s*(?P<yield>\d+)')
        recipe_yield = None
        recipe_yield_str = response.selector.xpath("//*[@class='nutrition-top light-underline']/text()").get()
        if recipe_yield_str:
            m = recipe_yield_re.match(recipe_yield_str)
            if m:
                recipe_yield = m.group('yield')
        return recipe_yield
         
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
                recipe_item['recipeIngredient'] = rp.get_recipe_ingredient()
                recipe_item['recipeInstructions'] = rp.get_recipe_instructions()
                #recipe_item['recipeYield'] = rp.get_recipe_yield()
                recipe_item['nutrition'] = rp.get_nutrition()
                recipe_item['recipeCategory'] = rp.get_recipe_category()
                recipe_item['aggregateRating'] = rp.get_rating()
                recipe_item['aggregateRating'].update({'ratingCount':rp.get_review_cnt()})
        else:
            recipe_item['name'] = self.__get_name(response)
            recipe_item['recipeIngredient'] = self.__get_ingredients(response)
            recipe_item['recipeInstructions'] = self.__get_instructions(response)
            recipe_item['recipeYield'] = self.__get_servings(response)
            recipe_item['nutrition'] = dict()
            recipe_item['nutrition']['calories'] = self.__get_calories(response)
            recipe_item['nutrition']['fatContent'] = self.__get_fat(response)
            recipe_item['nutrition']['proteinContent'] = self.__get_protein(response)
            recipe_item['nutrition']['cholesterolContent'] = self.__get_cholesterol(response)
            recipe_item['nutrition']['sodiumContent'] = self.__get_sodium(response)
            recipe_item['recipeCategory'] = self.__get_categories(response)
            recipe_item['aggregateRating'] = self.__get_rating(response)
            recipe_item['aggregateRating'].update({'ratingCount':self.__get_review_cnt(response)})

      
        if 'recipeYield' not in recipe_item: 
            recipe_item['recipeYield'] = self.__get_recipe_yield(response)
        elif recipe_item['recipeYield'] == None:
            recipe_item['recipeYield'] = self.__get_recipe_yield(response)
            
        if recipe_item.fields_populated():
            yield recipe_item

        allow_re = ['https://www.allrecipes\.com/recipe.*']
        deny_re = ['https://www.allrecipes\.com/recipe/\d+/.*/reviews/.*','https://www.allrecipes\.com/recipe/\d+/.*/photos/.*']
        links = LinkExtractor(allow=allow_re, deny=deny_re, allow_domains=['allrecipes.com'], unique=True).extract_links(response)
        for link in links:
            if link is not None:
                yield response.follow(link, callback=self.parse)

