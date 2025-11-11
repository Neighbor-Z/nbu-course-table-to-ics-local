from utils.handler import handleIcs
import requests
import tkinter.messagebox
import traceback
import sys

def register(usr,pwd,first_monday,XNXQDM):
    try:
        url, data_hash = handleIcs(usr, pwd, first_monday, XNXQDM)
    except Exception as ee:
        if str(ee) == '帐号或密码错误':
            if sys.platform=="win32":
                print(ee)
            else:
                traceback.print_exc()
            tkinter.messagebox.showerror('错误','帐号或密码错误')
        elif str(ee) == '需要验证码':
            if sys.platform=="win32":
                print(ee)
            else:
                traceback.print_exc()
            tkinter.messagebox.showerror('错误','可能重复登录次数太多需要验证码。请用网页打开网上办事大厅登陆一次')
        elif str(ee) == '未排课':
            if sys.platform=="win32":
                print(ee)
            else:
                traceback.print_exc()
            tkinter.messagebox.showerror('错误','您课表排课数据为空，可能是未选课或教务处未排课')
        else:
            if sys.platform=="win32":
                print(ee)
            else:
                traceback.print_exc()
            tkinter.messagebox.showerror('错误','其他错误，参见控制台')
