from utils.handler import handleIcs
import traceback
import sys

def register(usr,pwd,first_monday,XNXQDM):
    """
    注册函数，不再使用tkinter.messagebox（因为可能在非主线程中调用）
    异常会被抛出，由调用者处理
    返回日历对象，而不是直接保存文件
    """
    try:
        calendar, data_hash = handleIcs(usr, pwd, first_monday, XNXQDM)
        return calendar, data_hash
    except Exception as ee:
        # 打印错误信息到控制台
        if sys.platform=="win32":
            print(ee)
        else:
            traceback.print_exc()
        
        # 根据错误类型构造友好的错误消息
        if str(ee) == '帐号或密码错误':
            error_msg = '帐号或密码错误'
        elif str(ee) == '需要验证码':
            error_msg = '可能重复登录次数太多需要验证码。请用网页打开网上办事大厅登陆一次'
        elif str(ee) == '未排课':
            error_msg = '您课表排课数据为空，可能是未选课或教务处未排课'
        else:
            error_msg = f'其他错误：{str(ee)}'
        
        # 重新抛出异常，让调用者（Worker线程）通过信号发送到主线程处理
        raise Exception(error_msg)
