import datetime

CONFIG_DATA = {
    "ksjcsj": [
        {"jc": 1, "hours": 8, "minutes": 0},
        {"jc": 2, "hours": 8, "minutes": 50},
        {"jc": 3, "hours": 10, "minutes": 0},
        {"jc": 4, "hours": 10, "minutes": 50},
        {"jc": 5, "hours": 13, "minutes": 30},
        {"jc": 6, "hours": 14, "minutes": 20},
        {"jc": 7, "hours": 15, "minutes": 30},
        {"jc": 8, "hours": 16, "minutes": 20},
        {"jc": 9, "hours": 18, "minutes": 0},
        {"jc": 10, "hours": 18, "minutes": 50},
        {"jc": 11, "hours": 19, "minutes": 40},
        {"jc": 12, "hours": 20, "minutes": 30}
    ],
    "jsjcsj": [
        {"jc": 1, "hours": 8, "minutes": 45},
        {"jc": 2, "hours": 9, "minutes": 35},
        {"jc": 3, "hours": 10, "minutes": 45},
        {"jc": 4, "hours": 11, "minutes": 35},
        {"jc": 5, "hours": 14, "minutes": 15},
        {"jc": 6, "hours": 15, "minutes": 5},
        {"jc": 7, "hours": 16, "minutes": 15},
        {"jc": 8, "hours": 17, "minutes": 5},
        {"jc": 9, "hours": 18, "minutes": 45},
        {"jc": 10, "hours": 19, "minutes": 35},
        {"jc": 11, "hours": 20, "minutes": 25},
        {"jc": 12, "hours": 21, "minutes": 15}
    ],
    "msksjcsj": [
        {"jc": 1, "hours": 8, "minutes": 30},
        {"jc": 2, "hours": 9, "minutes": 20},
        {"jc": 3, "hours": 10, "minutes": 20},
        {"jc": 4, "hours": 11, "minutes": 10},
        {"jc": 5, "hours": 13, "minutes": 30},
        {"jc": 6, "hours": 14, "minutes": 20},
        {"jc": 7, "hours": 15, "minutes": 20},
        {"jc": 8, "hours": 16, "minutes": 10},
        {"jc": 9, "hours": 18, "minutes": 0},
        {"jc": 10, "hours": 18, "minutes": 50},
        {"jc": 11, "hours": 19, "minutes": 40},
        {"jc": 12, "hours": 20, "minutes": 25}
    ],
    "msjsjcsj": [
        {"jc": 1, "hours": 9, "minutes": 15},
        {"jc": 2, "hours": 10, "minutes": 5},
        {"jc": 3, "hours": 11, "minutes": 5},
        {"jc": 4, "hours": 11, "minutes": 55},
        {"jc": 5, "hours": 14, "minutes": 15},
        {"jc": 6, "hours": 15, "minutes": 5},
        {"jc": 7, "hours": 16, "minutes": 5},
        {"jc": 8, "hours": 16, "minutes": 55},
        {"jc": 9, "hours": 18, "minutes": 45},
        {"jc": 10, "hours": 19, "minutes": 35},
        {"jc": 11, "hours": 20, "minutes": 25},
        {"jc": 12, "hours": 21, "minutes": 15}
    ]
}

def getYamlData():
    return CONFIG_DATA

def getKSJCtime(week, day, ksjc, loc, first_monday):
    time_config = getYamlData()
    delta_days = (week - 1) * 7 + day - 1
    if "梅山" in loc:
        delta_hours = time_config['msksjcsj'][ksjc - 1]['hours']
        delta_minutes = time_config['msksjcsj'][ksjc - 1]['minutes']
    else:
        delta_hours = time_config['ksjcsj'][ksjc - 1]['hours']
        delta_minutes = time_config['ksjcsj'][ksjc - 1]['minutes']
#   f_m = datetime.datetime.strptime(time_config['first_monday'], '%Y-%m-%d')
    f_m = datetime.datetime.strptime(first_monday, '%Y-%m-%d')
    return f_m + datetime.timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)


def getJSJCtime(week, day, jsjc, loc, first_monday):
    time_config = getYamlData()
    delta_days = (week - 1) * 7 + day - 1
    if "梅山" in loc:
        delta_hours = time_config['msjsjcsj'][jsjc - 1]['hours']
        delta_minutes = time_config['msjsjcsj'][jsjc - 1]['minutes']
    else:
        delta_hours = time_config['jsjcsj'][jsjc - 1]['hours']
        delta_minutes = time_config['jsjcsj'][jsjc - 1]['minutes']
#   f_m = datetime.datetime.strptime(time_config['first_monday'], '%Y-%m-%d')
    f_m = datetime.datetime.strptime(first_monday, '%Y-%m-%d')
    return f_m + datetime.timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)

