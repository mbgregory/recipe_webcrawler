import datetime
import re

class SchemaUtilities:
    @staticmethod
    def parse_iso8601_duration(iso8601_duration_str):
        duration = None 
        duration_re = re.compile(r'P((?P<years>\d+)Y)?((?P<months>\d+)M)?((?P<days>\d+)D)?'
                                  '(T((?P<hours>\d+)H)?((?P<minutes>\d+)M)((?P<seconds>\d+\.?\d*)S)?)?$')
                                  
        m = duration_re.match(iso8601_duration_str)
        if m:
            weeks = int(m.group('years'))*52 if m.group('years') else 0     
            weeks += int(m.group('months'))*4 if m.group('months') else 0     
            days = int(m.group('days')) if m.group('days') else 0
            hours = int(m.group('hours')) if m.group('hours') else 0
            minutes = int(m.group('minutes')) if m.group('minutes') else 0
            seconds_str = m.group('seconds') if m.group('seconds') else '0'
            seconds = 0
            milliseconds = 0
            if seconds_str != '0':
                if '.' in seconds_str:
                    seconds = int(seconds_str.split('.')[0])
                    milliseconds = int(seconds_str.split('.')[1])
                else:
                    seconds = int(seconds_str)

            duration = datetime.timedelta(
                            weeks=weeks,
                            days=days,
                            hours=hours,
                            minutes=minutes,
                            seconds=seconds,
                            milliseconds=milliseconds,
                       )

        return duration
