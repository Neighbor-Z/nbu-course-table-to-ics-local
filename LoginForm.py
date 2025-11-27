import customtkinter as ctk
import tkinter.messagebox
import sys, webbrowser
from app.index import register


def action():
    try:
        if data1.get()=='' or data2.get()=='' or data3.get()=='':
            tkinter.messagebox.showerror('错误','请正确填写信息')
            result.set("失败")
            resultBar=ctk.CTkLabel(root,textvariable=result,font=('微软雅黑',14), 
                                    fg_color="#dcdbdb", 
                                    text_color="#e90000")
        else:
            result.set("你可以在控制台中看到实时作业进度")
            resultBar=ctk.CTkLabel(root,textvariable=result,font=('微软雅黑',14),fg_color="#dcdbdb")
            username=data1.get()
            password=data2.get()
            first_monday=data3.get()
            XNXQDM=data4.get()
            calendar, data_hash=register(username, password, first_monday, XNXQDM)
            try:
            # 保存文件
                calendar.save_as_ics_file()
                print("文件已保存")
            except Exception as e:
                print("保存失败")
        # resultBar.place(x=60, y=320)
    except Exception as e:
        # 捕获所有未预期的异常，防止程序崩溃
        error_msg = f"错误: {str(e)}"
        tkinter.messagebox.showerror('错误', error_msg)
        result.set("操作失败，请查看控制台错误信息")


def openweb():
    webbrowser.open("https://github.com/Neighbor-Z/nbu-course-table-to-ics-local/")


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("宁波大学课表工具 v1.5 CustomTkinter")
    root.geometry("520x340+600+300")
    root.minsize(320, 320)
    if sys.platform=="win32":
        ctk.set_appearance_mode("Dark")
        switch_var = ctk.StringVar(value="on")
    elif sys.platform=="linux":
        ctk.set_appearance_mode("light")
        switch_var = ctk.StringVar(value="off")
        # HiDPI Linux Display Support
        ctk.set_widget_scaling(1.5)  # widget dimensions and text size
        ctk.set_window_scaling(1.5)  # window geometry dimensions
    else:
        ctk.set_appearance_mode("light")
        switch_var = ctk.StringVar(value="off")
    ctk.set_default_color_theme("blue")

    # =============================
    # Main container
    # =============================
    main = ctk.CTkFrame(root, corner_radius=10)
    main.pack(fill="both", expand=True, padx=10, pady=10)

    # =============================
    # Top bar (theme switch)
    # =============================
    top_bar = ctk.CTkFrame(main)
    top_bar.pack(fill="x", pady=(5, 15))
    
    def _apply_appearance(mode: str):
        # Apply appearance mode and refresh pending UI updates to reduce visible flicker.
        ctk.set_appearance_mode(mode)
        try:
            root.update_idletasks()
        except Exception:
            pass

    def on_theme_toggle():
        if switch_var.get()=="on":
            mode = "Dark"
        else:
            mode = "Light"
        try:
            _apply_appearance(mode)
        except Exception:
            pass

    theme_switch = ctk.CTkSwitch(top_bar, text="深色", command=on_theme_toggle,
                                 variable=switch_var, 
                                 font=('微软雅黑',12),
                                 onvalue="on", offvalue="off")
    theme_switch.pack(side="left", padx=(5, 2))

    # =============================
    # Form container (two-column layout)
    # 左列：学号、密码；右列：学期、首个周一
    # =============================
    form = ctk.CTkFrame(main)
    form.pack(fill="x", expand=False, pady=(10, 10))
    # Grid layout: 2 columns
    for col in range(2):
        form.grid_columnconfigure(col, weight=1)

    data1 = ctk.StringVar()
    data2 = ctk.StringVar()
    data3 = ctk.StringVar()
    data4 = ctk.StringVar()
    result= ctk.StringVar()
    data3.set("2025-09-08")
    data4.set("2025-2026-1")
    if sys.platform=="win32":
        dL1=ctk.CTkLabel(form, text="学号", font=('微软雅黑',12))
        dL2=ctk.CTkLabel(form, text="学期", font=('微软雅黑',12))
        dL3=ctk.CTkLabel(form, text="密码", font=('微软雅黑',12))
        dL4=ctk.CTkLabel(form, text="首个周一", font=('微软雅黑',12))
    else:
        dL1=ctk.CTkLabel(form, text="学号")
        dL2=ctk.CTkLabel(form, text="学期")
        dL3=ctk.CTkLabel(form, text="密码")
        dL4=ctk.CTkLabel(form, text="首个周一")

    # 左列：学号、密码（垂直堆叠）
    dL1.grid(row=0, column=0, padx=8, pady=(8,2), sticky="w")
    entry1=ctk.CTkEntry(form, textvariable=data1)
    entry1.grid(row=1, column=0, padx=8, pady=(0,8), sticky="ew")

    dL3.grid(row=2, column=0, padx=8, pady=(8,2), sticky="w")
    entry3=ctk.CTkEntry(form, textvariable=data2, show="*")
    entry3.grid(row=3, column=0, padx=8, pady=(0,8), sticky="ew")

    # 右列：学期、首个周一（垂直堆叠）
    dL2.grid(row=0, column=1, padx=8, pady=(8,2), sticky="w")
    entry2=ctk.CTkEntry(form, textvariable=data4)
    entry2.grid(row=1, column=1, padx=8, pady=(0,8), sticky="ew")

    dL4.grid(row=2, column=1, padx=8, pady=(8,2), sticky="w")
    entry4=ctk.CTkEntry(form, textvariable=data3)
    entry4.grid(row=3, column=1, padx=8, pady=(0,8), sticky="ew")

    # =============================
    # Button area (保留“获取”按钮)
    # =============================
    bottom_bar = ctk.CTkFrame(main)
    bottom_bar.pack(pady=(20, 5))
    btn=ctk.CTkButton(bottom_bar, text=" 获取 ", command=action, font=('微软雅黑',14), width=120)
    btn.pack()

    # 右下角的 GitHub 文本链接（无按钮背景，仅下划线）
    try:
        # place inside `main` so background matches rounded container and avoids visible rectangle artifacts
        main_bg = main.cget('fg_color') if main.cget('fg_color') is not None else None
        github_label = ctk.CTkLabel(main, text='GitHub', text_color="#1a73e8", fg_color=main_bg, font=('微软雅黑',14,'underline'))
        github_label.place(relx=0.98, rely=0.98, anchor="se")
        github_label.bind("<Button-1>", lambda e: openweb())
    except Exception:
        # fallback to a simple tkinter label if CTkLabel fails for any reason
        import tkinter as tk
        try:
            bg = main.cget('fg_color') or root.cget('bg')
        except Exception:
            bg = root.cget('bg')
        github_label = tk.Label(main, text="GitHub", fg="#1a73e8", bg=bg, cursor="hand2", font=('微软雅黑',14,'underline'))
        github_label.place(relx=0.98, rely=0.98, anchor="se")
        github_label.bind("<Button-1>", lambda e: openweb())

    root.mainloop()

