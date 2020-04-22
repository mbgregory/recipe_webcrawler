import re

class NutritionInformationParser:

    def __init__(self, nutrition_obj):
        self._nutrition_obj = nutrition_obj
        self._nutrition_info = dict()

        self._nutrition_re = re.compile(r'^(?P<quantity>\d+\.?\d*)\s*(?P<unit>\w*)')
        nutrition_parser = {
            'calories':self._parse_nutrition_string,
            'carbohydrateContent':self._parse_nutrition_string,
            'cholesterolContent':self._parse_nutrition_string,
            'fatContent':self._parse_nutrition_string,
            'fiberContent':self._parse_nutrition_string,
            'proteinContent':self._parse_nutrition_string,
            'saturatedFatContent':self._parse_nutrition_string,
            #'servingSize':
            'sodiumContent':self._parse_nutrition_string,
            'sugarContent':self._parse_nutrition_string,
            'transFatContent':self._parse_nutrition_string,
            'unsaturatedFatContent':self._parse_nutrition_string
        }

        for key,func in nutrition_parser.items():
            if key in self._nutrition_obj:
                func(self._nutrition_obj[key], key)

    def _parse_nutrition_string(self, nutrition_str, nutrition_key):
        default_unit = {
            'calories':'calories',
            'carbohydrateContent':'g',
            'cholesterolContent':'g',
            'fatContent':'g',
            'fiberContent':'g',
            'proteinContent':'g',
            'saturatedFatContent':'g',
            #'servingSize':
            'sodiumContent':'mg',
            'sugarContent':'g',
            'transFatContent':'g',
            'unsaturatedFatContent':'g',
        }
            
        self._nutrition_info[nutrition_key] = None
        if nutrition_str is not None:
            m = self._nutrition_re.match(nutrition_str)
            if m:
                if m.group('quantity') and m.group('unit'):
                    self._nutrition_info[nutrition_key] = float(m.group('quantity'))
                elif m.group('quantity'):
                    self._nutrition_info[nutrition_key] = float(m.group('quantity'))
                        
            #if m:
            #    if m.group('quantity') and m.group('unit'):
            #        self._nutrition_info[nutrition_key] = {
            #            'quantity':float(m.group('quantity')),
            #            'unit':m.group('unit')
            #        }       
            #    elif m.group('quantity'):
            #        self._nutrition_info[nutrition_key] = {
            #            'quantity':float(m.group('quantity')),
            #            'unit':default_unit[key]
            #        }

    def get_calories(self):
        return self._nutrition_info['calories'] if 'calories' in self._nutrition_info else None

    def get_carbohydrates(self):
        return self._nutrition_info['carbohydrateContent'] if 'carbohydrateContent'in self._nutrition_info  else None

    def get_cholesterol(self):
        return self._nutrition_info['cholesterolContent'] if 'cholesterolContent' in self._nutrition_info else None

    def get_fat(self):
        return self._nutrition_info['fatContent'] if 'fatContent' in self._nutrition_info else None

    def get_fiber(self):
        return self._nutrition_info['fiberContent'] if 'fiberContent' in self._nutrition_info else None

    def get_protein(self):
        return self._nutrition_info['proteinContent'] if 'proteinContent' in self._nutrition_info else None

    def get_saturated_fat(self):
        return self._nutrition_info['saturatedFatContent'] if 'saturatedFatContent' in self._nutrition_info else None

    def get_sodium(self):
        return self._nutrition_info['sodiumContent'] if 'sodiumContent' in self._nutrition_info else None

    def get_sugar(self):
        return self._nutrition_info['sugarContent'] if 'sugarContent' in self._nutrition_info else None

    def get_trans_fat(self):
        return self._nutrition_info['transFatContent'] if 'transFatContent' in self._nutrition_info else None

    def get_unsaturated_fat(self):
        return self._nutrition_info['unsaturatedFatContent'] if 'unsaturatedFatContent' in self._nutrition_info else None

    def get_nutrition(self):
        nutrition_info = dict()
        all_nutrition_info = {
            'calories':self.get_calories,
            'carbohydrateContent':self.get_carbohydrates,
            'cholesterolContent':self.get_cholesterol,
            'fatContent':self.get_fat,
            'fiberContent':self.get_fiber,
            'proteinContent':self.get_protein,
            'saturatedFatContent':self.get_saturated_fat,
            #'servingSize':
            'sodiumContent':self.get_sodium,
            'sugarContent':self.get_sugar,
            'transFatContent':self.get_trans_fat,
            'unsaturatedFatContent':self.get_unsaturated_fat
        }

        for key,func in all_nutrition_info.items():
            if key in self._nutrition_obj:
                nutrition_info[key] = func()
        return nutrition_info
