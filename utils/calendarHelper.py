import datetime
import os
import uuid
try:
    import tkinter.filedialog
except ImportError:
    tkinter = None

class Event:
    """
    事件对象
    """

    def __init__(self, kwargs):
        self.event_data = kwargs

    def __turn_to_string__(self):
        self.event_text = "BEGIN:VEVENT\n"
        for item, data in self.event_data.items():
            item = str(item).replace("_", "-")
            if item not in ["ORGANIZER", "DTSTART", "DTEND"]:
                self.event_text += "%s:%s\n" % (item, data)
            else:
                self.event_text += "%s:%s\n" % (item, data)
        self.event_text += "END:VEVENT\n"
        return self.event_text


class Calendar:
    """
    日历对象
    """

    def __init__(self, calendar_name="宁波大学课程表"):
        self.__events__ = {}
        self.__event_id__ = 0
        self.calendar_name = calendar_name

    def add_event(self, **kwargs):
        event = Event(kwargs)
        event_id = self.__event_id__
        self.__events__[self.__event_id__] = event
        self.__event_id__ += 1
        return event_id

    def modify_event(self, event_id, **kwargs):
        for item, data in kwargs.items():
            self.__events__[event_id].event_data[item] = data

    def remove_event(self, event_id):
        self.__events__.pop(event_id)

    def get_ics_text(self):
        self.__calendar_text__ = """BEGIN:VCALENDAR\nPRODID:-//NeighborhoodOfZ//NBU Class Table//CN\nVERSION:2.0\nCALSCALE:GREGORIAN\nMETHOD:PUBLISH\nX-WR-CALNAME:%s\nX-WR-TIMEZONE:Asia/Shanghai\nX-WR-CALDESC:%s 更新时间：%s\n""" % (
            self.calendar_name, self.calendar_name, datetime.datetime.today().strftime(
                "%Y%m%dT%H%M%SZ")) + """BEGIN:VTIMEZONE\nTZID:Asia/Shanghai\nX-LIC-LOCATION:Asia/Shanghai\nBEGIN:STANDARD\nTZOFFSETFROM:+0800\nTZOFFSETTO:+0800\nTZNAME:CST\nDTSTART:19700101T000000\nEND:STANDARD\nEND:VTIMEZONE\n"""
        for key, value in self.__events__.items():
            self.__calendar_text__ += value.__turn_to_string__()
        self.__calendar_text__ += "END:VCALENDAR"
        return self.__calendar_text__

    def save_as_ics_file(self, save_path=None):
        ics_text = self.get_ics_text()
        if save_path is None:
            # 如果没有提供路径，使用 tkinter 对话框（向后兼容）
            if tkinter is None:
                raise ValueError("未提供保存路径，且 tkinter 不可用")
            print("请在弹出窗口中选择保存位置")
            filedir = tkinter.filedialog.askdirectory(initialdir="/", title="选择保存路径")
            if not filedir:
                raise ValueError("未选择保存路径")
            save_path = f"{filedir}/{self.calendar_name}.ics"
        else:
            # 如果提供了路径，直接使用
            if not save_path.endswith('.ics'):
                # 如果路径是目录，添加文件名
                if not save_path.endswith('/') and not save_path.endswith('\\'):
                    save_path += '/'
                save_path = f"{save_path}{self.calendar_name}.ics"
        
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(ics_text)  # 使用utf8编码生成ics文件，否则日历软件打开是乱码
        return save_path

    def open_ics_file(self):
        os.system("%s.ics" % self.calendar_name)


def add_event(cal, SUMMARY, DTSTART, DTEND, DESCRIPTION, LOCATION):
    """
    向Calendar日历对象添加事件的方法
    :param cal: calender日历实例
    :param SUMMARY: 事件名
    :param DTSTART: 事件开始时间
    :param DTEND: 时间结束时间
    :param DESCRIPTION: 备注
    :param LOCATION: 时间地点
    :return:
    """
    # TZID=Asia/Shanghai:
    time_format = "{date.year}{date.month:0>2d}{date.day:0>2d}T{date.hour:0>2d}{date.minute:0>2d}00"
    dt_start = time_format.format(date=DTSTART)
    dt_end = time_format.format(date=DTEND)
    create_time = datetime.datetime.today().strftime("%Y%m%dT%H%M%SZ")
    cal.add_event(
        ORGANIZER="CN=宁波大学课程表:mailto:Neighborhood-of-Z",
        DTSTART=dt_start,
        DTEND=dt_end,
        DTSTAMP=create_time,
        UID="{}-Neighborhood-of-Z".format(uuid.uuid1()),
        CREATED=create_time,
        DESCRIPTION=DESCRIPTION,
        LAST_MODIFIED=create_time,
        SEQUENCE="0",
        LOCATION=LOCATION,
        STATUS="CONFIRMED",
        SUMMARY=SUMMARY,
        TRANSP="TRANSPARENT"
    )
    