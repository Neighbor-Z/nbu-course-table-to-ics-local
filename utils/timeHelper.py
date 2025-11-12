import datetime

try:
    import yaml

    def getYamlData():
        with open('config.yml', 'r', encoding='utf-8') as file:
            return yaml.load(file, Loader=yaml.FullLoader)

except ModuleNotFoundError:
    # 优先使用 PyYAML；若不可用则使用简易回退解析器
    # 该解析器针对本项目简单的 config.yml 结构：顶层键对应一个包含内联映射的列表，示例：
    # ksjcsj:
    #   - {jc: 1,hours: 8,minutes: 0}
    def _parse_inline_mapping(s: str):
        s = s.strip()
        if s.startswith('{') and s.endswith('}'):
            s = s[1:-1]
        parts = [p.strip() for p in s.split(',') if p.strip()]
        d = {}
        for part in parts:
            if ':' not in part:
                continue
            k, v = part.split(':', 1)
            k = k.strip()
            v = v.strip()
            # 尝试转换为 int，否则保留为字符串
            try:
                v2 = int(v)
            except Exception:
                v2 = v
            d[k] = v2
        return d

    def getYamlData():
        data = {}
        current_key = None
        with open('config.yml', 'r', encoding='utf-8') as f:
            for raw in f:
                line = raw.rstrip('\n')
                if not line.strip():
                    continue
                # 忽略 YAML 注释行
                if line.startswith('#'):
                    continue
                if ':' in line and not line.startswith(' '):
                    # 例如："ksjcsj:"
                    current_key = line.split(':', 1)[0].strip()
                    data[current_key] = []
                    continue
                # 列表项，内联映射
                if current_key is not None and ('-' in line):
                    # 提取 '-' 之后的部分
                    idx = line.find('-')
                    rest = line[idx+1:].strip()
                    entry = _parse_inline_mapping(rest)
                    if entry:
                        data[current_key].append(entry)
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
