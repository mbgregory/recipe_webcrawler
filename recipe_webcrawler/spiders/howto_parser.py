from recipe_webcrawler.spiders.schema_utilities import SchemaUtilities

class HowToParser:
    def __init__(self, howto_obj):
        self._howto_obj = howto_obj
        self._howto_info = dict()

        howto_parser = {
            'prepTime':self._parse_time,
            'totalTime':self._parse_time,
        }
        
        for key,func in howto_parser.items():
            if key in self._howto_obj:
                func(self._howto_obj[key], key)

    def _parse_time(self, time_str, key):
        time = SchemaUtilities.parse_iso8601_duration(time_str)
        self._howto_info[key] = time

    def get_prep_time(self):
        return self._howto_info['prepTime'] if 'prepTime' in self._howto_info else None

    def get_total_time(self):
        return self._howto_info['totalTime'] if 'totalTime' in self._howto_info else None
