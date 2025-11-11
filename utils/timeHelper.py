import datetime
import yaml


def getYamlData():
    file = open('config.yml', 'r', encoding='utf-8')
    file_data = file.read()
    file.close()
    data = yaml.load(file_data, Loader=yaml.FullLoader)
    return data


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

# print(getJSJCtime(4, 3, 12))
