from tkinter import *
import sys
import tkinter.messagebox
import sv_ttk
from tkinter import ttk
from app.index import register

root = Tk()
style = ttk.Style()
if sys.platform=="win32":
    sv_ttk.set_theme("dark")
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1) #告诉操作系统使用程序自身的dpi适配
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0) #获取屏幕的缩放因子
    root.tk.call('tk', 'scaling', ScaleFactor/75) #设詈程序缩放
else:
    sv_ttk.set_theme("light")

def on_switch_toggle():
    if switchState.get():
        sv_ttk.set_theme("dark")
    else:
        sv_ttk.set_theme("light")

def calClick(): 
    if data1.get()=='' or data2.get()=='' or data3.get()=='':
        tkinter.messagebox.showerror('错误','请正确填写信息')
        result.set("失败")
        resultBar=Label(root,textvariable=result,font='微软雅黑 14 bold',fg='#e90000')
    else:
        result.set("你可以在控制台中看到实时作业进度")
        resultBar=Label(root,textvariable=result)
        username=data1.get()
        password=data2.get()
        first_monday=data3.get()
        XNXQDM=data4.get()
        register(username, password, first_monday, XNXQDM)
    if sys.platform=="win32" or sys.platform=="linux":
        resultBar.place(x=60, y=340)
    else:
        resultBar.place(x=30, y=170)
    

# 支持命令行参数
# if __name__ == "__main__" and len(sys.argv) > 1:
#     if sys.argv[1] == "-h" or sys.argv[1] == "--help":
#         print("USAGE: loginform [username password] [first_monday term]")
#         sys.exit()
#     elif sys.argv[1] == '':
#         root.after(300, calClick)
#         root.after(2000, root.destroy)
#     else:
#         print("unknown argument!")
#         print("USAGE: loginform [username password first_monday term]")
#         sys.exit()
    
if __name__ == '__main__':
    root.title("宁波大学课表工具 v1.4")
    # 设置字体
    if sys.platform=="win32" or sys.platform=="linux":
        # style.configure("TEntry", font=('宋体', 15))
        style.configure('TButton',font=('微软雅黑', 10), width=10)
        # style.configure("TCheckbutton", font="微软雅黑 24")
        # style.configure("Label", font=('宋体', 12))
        # style.configure("big.TLabel", font="微软雅黑 36")
        # style.configure("small.TLabel", font="微软雅黑 20")
        # style.configure("verysmall.TLabel", font="微软雅黑 20")
        root.geometry('820x440+600+300')
    else:
        # style.configure("TEntry", font="微软雅黑 12")
        # style.configure("TButton", font="微软雅黑 12")
        # style.configure("TCheckbutton", font="微软雅黑 12")
        # style.configure("TLabel", font="微软雅黑 12")
        # style.configure("big.TLabel", font="微软雅黑 18")
        # style.configure("small.TLabel", font="微软雅黑 10")
        # style.configure("verysmall.TLabel", font="微软雅黑 10")
        root.geometry('410x220+600+300')
    root.resizable(width=False, height=False)
    infoLabel=Label(root, text='请使用网上办事大厅账号登录',font='微软雅黑 16')
    devLabel=Label(root, text='By z邻域')
    switchState=BooleanVar()
    themeSwitch=ttk.Checkbutton(root, variable=switchState, style="Switch.TCheckbutton", command=on_switch_toggle)
    data1=StringVar()
    data2=StringVar()
    data3=StringVar()
    data4=StringVar()
    result=StringVar()
    data3.set("2025-09-08")
    data4.set("2025-2026-1")
    calButton=ttk.Button(root, text="  获取!  ",command=calClick,style="Accent.TButton")
    if sys.platform=="win32" or sys.platform=="linux":
        # 深色模式切换开关
        themeSwitch.place(x=680, y=40)
        infoLabel.place(x=35, y=40)
        devLabel.place(x=560, y=360)
        dataLabel1=Label(root, text='学号', font='微软雅黑 10')
        dL2=Label(root, text='密码', font='微软雅黑 10')
        dL3=Label(root, text='首个周一', font='微软雅黑 10')
        dL4=Label(root, text='学期', font='微软雅黑 10')
        dataLabel1.place(x=40, y=130)
        dL2.place(x=40, y=210)
        dL3.place(x=40, y=290)
        dL4.place(x=440, y=130)
        entry1=ttk.Entry(root,textvariable=data1,font=('Helvetica', 10),width=12)
        entry2=ttk.Entry(root,textvariable=data2,font=('Helvetica', 10),show='*',width=12)
        entry3=ttk.Entry(root,textvariable=data3,font=('Helvetica', 10),width=10)
        entry4=ttk.Entry(root,textvariable=data4,font=('Helvetica', 10),width=12)
        entry1.place(x=160 ,y=130)
        entry2.place(x=160 ,y=210)
        entry3.place(x=160 ,y=290)
        entry4.place(x=520 ,y=130)
        calButton.place(x=480, y=280)
    else:
        themeSwitch.place(x=340, y=20)
        infoLabel.place(x=17, y=20)
        devLabel.place(x=280, y=180)
        dataLabel1=ttk.Label(root, text='学号')
        dL2=ttk.Label(root, text='密码')
        dL3=ttk.Label(root, text='首个周一')
        dL4=ttk.Label(root, text='学期')
        dataLabel1.place(x=20, y=65)
        dL2.place(x=20, y=105)
        dL3.place(x=20, y=145)
        dL4.place(x=220, y=65)
        entry1=ttk.Entry(root,textvariable=data1,width=12)
        entry2=ttk.Entry(root,textvariable=data2,show='*',width=12)
        entry3=ttk.Entry(root,textvariable=data3,width=10)
        entry4=ttk.Entry(root,textvariable=data4,width=12)
        entry1.place(x=80 ,y=60)
        entry2.place(x=80 ,y=100)
        entry3.place(x=80 ,y=140)
        entry4.place(x=260 ,y=60)
        calButton.place(x=280, y=140)
    entry2.bind("<Return>", lambda e: calClick())
    root.mainloop()
    