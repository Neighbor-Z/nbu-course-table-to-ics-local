from tkinter import *
import sys
import tkinter.messagebox
import sv_ttk
from tkinter import ttk
from app.index import register

root = Tk()
frame = Frame(root)  # 创建一个Frame来容纳内容
frame.pack(fill=BOTH, expand=True)  # 让Frame填充整个窗口空间
style = ttk.Style()
# 主题开关状态在初始化时就设置，这样 UI 开关的状态会与实际主题保持一致。
# 在 Windows 上默认使用深色主题，并把 switchState 置为 True；其它平台默认浅色并置为 False。
switchState=BooleanVar()
if sys.platform=="win32":
    switchState.set(True)
    sv_ttk.set_theme("dark")
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1) #告诉操作系统使用程序自身的dpi适配
    ScaleFactor=ctypes.windll.shcore.GetScaleFactorForDevice(0) #获取屏幕的缩放因子
    root.tk.call('tk', 'scaling', ScaleFactor/75) #设詈程序缩放
else:
    switchState.set(False)
    sv_ttk.set_theme("light")

def apply_button_styles(is_dark: bool | None = None):
    try:
        if is_dark is None:
            try:
                th = style.theme_use() or ''
                is_dark = 'dark' in th.lower()
            except Exception:
                is_dark = False

        if sys.platform=="win32":
            for widget in frame.winfo_children():  # 移除frame中的所有小部件
                widget.destroy()
            if is_dark:
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")
            style.configure('TButton',font=('微软雅黑', 10), width=10)
            newcalButton=ttk.Button(frame, text="  获取!  ",command=calClick,style="Accent.TButton")
            newcalButton.place(x=480, y=280)
        else:
            if is_dark:
                sv_ttk.set_theme("dark")
            else:
                sv_ttk.set_theme("light")
    except Exception:
        pass

def on_switch_toggle():
    apply_button_styles(is_dark=switchState.get())

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
    
    
if __name__ == '__main__':
    root.title("宁波大学课表工具 v1.4.1")
    # 设置窗口大小
    if sys.platform=="win32" or sys.platform=="linux":
        root.geometry('820x440+600+300')
    else:
        root.geometry('410x220+600+300')
    root.resizable(width=False, height=False)
    infoLabel=Label(root, text='请使用网上办事大厅账号登录',font='微软雅黑 16')
    devLabel=Label(root, text='By z邻域')
    themeSwitch=ttk.Checkbutton(root, variable=switchState, style="Switch.TCheckbutton", command=on_switch_toggle)
    data1=StringVar()
    data2=StringVar()
    data3=StringVar()
    data4=StringVar()
    result=StringVar()
    data3.set("2025-09-08")
    data4.set("2025-2026-1")
    calButton=ttk.Button(frame, text="  获取!  ",command=calClick,style="Accent.TButton")
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
        style.configure('TButton',font=('微软雅黑', 10), width=10)
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
    