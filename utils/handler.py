from utils.timeHelper import getKSJCtime, getJSJCtime, getYamlData
from utils.kcbHelper import checkStudentKind, getClassListBks, getClassListYjs
from utils.calendarHelper import Calendar, add_event


def test():
    print("handler::", getYamlData())


def handleIcsBks(session,first_monday,XNXQDM):
    # with open('../test.json') as json_file:
    #     data_list = json.load(json_file)
    time_config = getYamlData()
    data_list, class_md5 = getClassListBks(session,XNXQDM)
    if len(data_list['datas']['xskcb']['rows']) == 0:
        raise ValueError('未排课')
    kcb_list = data_list['datas']['xskcb']['rows']
#   calendar = Calendar(calendar_name=kcb_list[0]['XH'] + '_' + time_config['XNXQDM'])
    calendar = Calendar(calendar_name=kcb_list[0]['XH'] + '_' + XNXQDM)
    for item in kcb_list:
        # print(kcb_list)
        # print("{}-{}-{}".format(item['JASMC'], item['KCM'], item['SKJS']))
        for (index, no_class) in enumerate(item['SKZC']):
            if int(no_class) == 1:
                if item['JASMC']==None:
                    item['JASMC']="无"
                add_event(calendar,
                          SUMMARY=item['KCM'],
                          DTSTART=getKSJCtime(index + 1, int(item['SKXQ']), int(item['KSJC']), item['JASMC'], first_monday),
                          DTEND=getJSJCtime(index + 1, int(item['SKXQ']), int(item['JSJC']), item['JASMC'], first_monday),
                          DESCRIPTION="教师：{}，节次：{}-{}，周次：{}，课号：{}".format(item['SKJS'], item['KSJC'], item['JSJC'],
                                                                          index + 1, item['KCH']),
                          LOCATION=item['JASMC'])
    url = calendar.save_as_ics_file()
    print("文件已保存。你可以安心关闭本窗口")
    return url, class_md5.hexdigest()


def handleIcsYjs(session,first_monday,XNXQDM):
    time_config = getYamlData()
    data_list, stu_info, class_md5 = getClassListYjs(session)
    kcb_list = data_list['datas']['xspkjgcx']['rows']
    calendar = Calendar(calendar_name=stu_info['data'][0]['XH'] + '_' + XNXQDM + '_YJS')
    for item in kcb_list:
        # print("{}-{}-{}".format(item['JASMC'], item['KCM'], item['SKJS']))
        for (index, no_class) in enumerate(item['ZCBH']):
            if int(no_class) == 1:
                add_event(calendar,
                          SUMMARY=item['KCMC'],
                          DTSTART=getKSJCtime(index + 1, int(item['XQ']), int(item['KSJCDM']), item['JASMC'], first_monday),
                          DTEND=getJSJCtime(index + 1, int(item['XQ']), int(item['JSJCDM']), item['JASMC'], first_monday),
                          DESCRIPTION="教师：{}，节次：{}-{}，周次：{}，课程代码：{}".format(item['JSXM'], item['KSJCDM'],
                                                                            item['JSJCDM'],
                                                                            index + 1, item['KCDM']),
                          LOCATION=item['JASMC'])
    url = calendar.save_as_ics_file()
    return url, class_md5.hexdigest()


def handleIcs(username, password, first_monday, XNXQDM):
    session = checkStudentKind(username, password)
    if len(username) == 9:
        res1, res2 = handleIcsBks(session,first_monday,XNXQDM)
    else:
        res1, res2 = handleIcsYjs(session,first_monday,'20251')
    return res1, res2
