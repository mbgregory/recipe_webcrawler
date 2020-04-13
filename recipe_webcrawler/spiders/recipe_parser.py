import json

from recipe_webcrawler.spiders.schema_utilities import SchemaUtilities
from recipe_webcrawler.spiders.nutrition_information_parser import NutritionInformationParser 
from recipe_webcrawler.spiders.howto_parser import HowToParser 

class RecipeParser:

    def __init__(self, json_str):
        self._completed = True
        try:
            self._recipe_obj = json.loads(json_str) 
        except json.decoder.JSONDecodeError:
            self._recipe_obj = None

        self._recipe_info = dict()

        recipe_parser = {
            'name':self._parse_recipe_name,
            'cookTime':self._parse_cook_time,
            #'cookingMethod':
            'nutrition':self._parse_nutrition,
            'recipeCategory':self._parse_recipe_category,
            'recipeCuisine':self._parse_recipe_cuisine,
            'recipeIngredient':self._parse_recipe_ingredient,
            'recipeInstructions':self._parse_recipe_instructions,
            'recipeYield':self._parse_recipe_yield,
            'prepTime':self._parse_prep_time,
            'totalTime':self._parse_total_time,
            'aggregateRating':self._parse_rating,
        }

        if self._recipe_obj:
            if type(self._recipe_obj) == list:
                for item in self._recipe_obj:
                    if '@type' in item:
                        if item['@type'] == 'Recipe':
                            for key,func in recipe_parser.items():
                                if key in item:
                                    func(item[key])
                        
            else:
                for key,func in recipe_parser.items():
                    if key in self._recipe_obj and key not in self._recipe_info:
                        func(self._recipe_obj[key])

        for key,func in recipe_parser.items():
            if key in self._recipe_info:
                if self._recipe_info[key] == None:
                    self._completed = False
            else:
                self._completed = False
                
                    

    def completed(self):
        return self._completed

    def _parse_recipe_name(self, name):
        self._recipe_info['name'] = name

    def get_recipe_name(self):
        return self._recipe_info['name'] if 'name' in self._recipe_info else None
 
    def _parse_cook_time(self, cook_time_str):
        cook_time = SchemaUtilities.parse_iso8601_duration(cook_time_str)
        self._recipe_info['cookTime'] = cook_time

    def get_cook_time(self):
        return self._recipe_info['cookTime'] if 'cookTime' in self._recipe_info else None

    def _parse_nutrition(self, nutrition_obj):
        np = NutritionInformationParser(nutrition_obj)
        self._recipe_info['nutrition'] =  np.get_nutrition()

    def get_nutrition(self):
        return self._recipe_info['nutrition'] if 'nutrition' in self._recipe_info else None

    def _parse_recipe_category(self, categories):
        category_list = categories
        if type(categories) is not list:
            category_list = [categories]

        self._recipe_info['recipeCategory'] = category_list
           
    def get_recipe_category(self):
        return self._recipe_info['recipeCategory'] if 'recipeCategory' in self._recipe_info else None
         
    def _parse_recipe_ingredient(self, ingredients):
        ingredients_list = ingredients
        if type(ingredients) is not list:
            ingredients_list = [ingredients]

        self._recipe_info['recipeIngredient'] = ingredients_list
           
    def _parse_recipe_yield(self, recipe_yield):
        self._recipe_info['recipeYield'] = recipe_yield 

    def get_recipe_yield(self):
        return self._recipe_info['recipeYield'] if 'recipeYield' in self._recipe_info else None

    def get_recipe_ingredient(self):
        return self._recipe_info['recipeIngredient'] if 'recipeIngredient' in self._recipe_info else None

    def _parse_recipe_instructions(self, instructions):
        instructions_str = ''
        if type(instructions) is not list:
            if 'text' in instructions: 
                instructions_str = [instructions['text']]
        else:
            for instruction in instructions:
                if 'text' in instruction:
                    instructions_str += instruction['text'] + ' '
            
        self._recipe_info['recipeInstructions'] = instructions_str.strip()
           
    def get_recipe_instructions(self):
        return self._recipe_info['recipeInstructions'] if 'recipeInstructions' in self._recipe_info else None

    def _parse_recipe_cuisine(self, cuisine):
        cuisine_list = cuisine
        if type(cuisine) is not list:
            cuisine_list = [cuisine]

        self._recipe_info['recipeCuisine'] = cuisine_list
           
    def get_recipe_cuisine(self):
        return self._recipe_info['recipeCuisine'] if 'recipeCuisine' in self._recipe_info else None

    def _parse_prep_time(self, prep_time_str):
        prep_time = SchemaUtilities.parse_iso8601_duration(prep_time_str)
        self._recipe_info['prepTime'] = prep_time

    def get_prep_time(self):
        return self._recipe_info['totalTime'] if 'totalTime' in self._recipe_info else None

    def _parse_total_time(self, total_time_str):
        total_time = SchemaUtilities.parse_iso8601_duration(total_time_str)
        self._recipe_info['totalTime'] = total_time

    def get_prep_time(self):
        return self._recipe_info['totalTime'] if 'totalTime' in self._recipe_info else None

    def _parse_rating(self, rating_info):
        self._recipe_info['aggregateRating'] = dict()
        self._recipe_info['aggregateRating']['value'] = rating_info['ratingValue']
        self._recipe_info['aggregateRating']['scale'] = rating_info['bestRating']
        self._recipe_info['aggregateRating']['review_cnt'] = rating_info['ratingCount']

    def get_rating(self):
        return {'value':self._recipe_info['aggregateRating']['value'], 'scale':self._recipe_info['aggregateRating']['scale']} if 'aggregateRating' in self._recipe_info else None

    def get_review_cnt(self):
        cnt = None
        if 'aggregateRating' in self._recipe_info:
            if 'review_cnt' in self._recipe_info['aggregateRating']:
                cnt = self._recipe_info['aggregateRating']['review_cnt']
        return cnt
