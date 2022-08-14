COLORS = [
    '#E0FFFF',  # light cyan
    '#FFE4E1',  # misty rose
    '#B0C4DE',  # light steel blue
    '#FFF5EE',  # seashell
    '#D8BFD8',  # thistle
    '#E6E6FA',  # lavender
    '#87CEFA',  # light sky blue
    '#D3D3D3',  # light grey
    '#F0E68C',  # khaki
    '#FFA07A',  # light salmon
]

FEED_ACTION = 'F'
WATER_ACTION = 'W'
NEVER = '0'
ONE_HOUR = '1'
ONE_DAY = '2'
ONE_WEEK = '3'
ONE_MONTH = '4'
OTHER_DAY = '5'
OTHER_WEEK = '6'
REPEAT_CHOICES = [
    (NEVER, 'never'),
    (ONE_HOUR, 'every hour'),
    (ONE_DAY, 'once a day'),
    (ONE_WEEK, 'once a week'),
    (ONE_MONTH, 'once a month'),
    (OTHER_DAY, 'once every 2 days'),
    (OTHER_WEEK, 'once every 2 weeks'),
]
