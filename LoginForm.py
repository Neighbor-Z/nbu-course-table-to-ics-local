import customtkinter as ctk
import tkinter.messagebox
import sys, webbrowser
from app.index import register
import threading


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("宁波大学课表工具 v1.5.1(2) CustomTkinter")
        self.root.geometry("520x360+600+300")
        self.root.minsize(320, 320)
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
        self.main = ctk.CTkFrame(self.root, corner_radius=10)
        self.main.pack(fill="both", expand=True, padx=10, pady=10)

        # =============================
        # Top bar (theme switch)
        # =============================
        self.top_bar = ctk.CTkFrame(self.main)
        self.top_bar.pack(fill="x", pady=(5, 15))
        
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

        self.theme_switch = ctk.CTkSwitch(self.top_bar, text="深色", command=on_theme_toggle,
                                     variable=switch_var, 
                                     font=('微软雅黑',12),
                                     onvalue="on", offvalue="off")
        self.theme_switch.pack(side="left", padx=(5, 2))

        # =============================
        # Form container (two-column layout)
        # 左列：学号、密码；右列：学期、首个周一
        # =============================
        self.form = ctk.CTkFrame(self.main)
        self.form.pack(fill="x", expand=False, pady=(10, 10))
        # Grid layout: 2 columns
        for col in range(2):
            self.form.grid_columnconfigure(col, weight=1)

        global data1 
        global data2 
        global data3 
        global data4 

        data1 = ctk.StringVar()
        data2 = ctk.StringVar()
        data3 = ctk.StringVar()
        data4 = ctk.StringVar()
        data3.set("2025-09-08")
        data4.set("2025-2026-1")
        if sys.platform=="win32":
            self.dL1=ctk.CTkLabel(self.form, text="学号", font=('微软雅黑',12))
            self.dL2=ctk.CTkLabel(self.form, text="学期", font=('微软雅黑',12))
            self.dL3=ctk.CTkLabel(self.form, text="密码", font=('微软雅黑',12))
            self.dL4=ctk.CTkLabel(self.form, text="首个周一", font=('微软雅黑',12))
        else:
            self.dL1=ctk.CTkLabel(self.form, text="学号")
            self.dL2=ctk.CTkLabel(self.form, text="学期")
            self.dL3=ctk.CTkLabel(self.form, text="密码")
            self.dL4=ctk.CTkLabel(self.form, text="首个周一")

        # 左列：学号、密码（垂直堆叠）
        self.dL1.grid(row=0, column=0, padx=8, pady=(8,2), sticky="w")
        self.entry1=ctk.CTkEntry(self.form, textvariable=data1)
        self.entry1.grid(row=1, column=0, padx=8, pady=(0,8), sticky="ew")

        self.dL3.grid(row=2, column=0, padx=8, pady=(8,2), sticky="w")
        self.entry3=ctk.CTkEntry(self.form, textvariable=data2, show="*")
        self.entry3.grid(row=3, column=0, padx=8, pady=(0,8), sticky="ew")

        # 右列：学期、首个周一（垂直堆叠）
        self.dL2.grid(row=0, column=1, padx=8, pady=(8,2), sticky="w")
        self.entry2=ctk.CTkEntry(self.form, textvariable=data4)
        self.entry2.grid(row=1, column=1, padx=8, pady=(0,8), sticky="ew")

        self.dL4.grid(row=2, column=1, padx=8, pady=(8,2), sticky="w")
        self.entry4=ctk.CTkEntry(self.form, textvariable=data3)
        self.entry4.grid(row=3, column=1, padx=8, pady=(0,8), sticky="ew")

        self.status_bar = ctk.CTkFrame(self.main)
        self.status_bar.pack(fill="x", pady=3)
        # 进度条
        self.progressBar=ctk.CTkProgressBar(self.status_bar, orientation="horizontal")
        self.progressBar.set(0)
        # 状态文本
        self.resultBar=ctk.CTkLabel(self.status_bar,font=('微软雅黑',14))
        self.resultBar.configure(text=" ")
        self.resultBar.pack()

        # =============================
        # Button area (保留“获取”按钮)
        # =============================
        self.bottom_bar = ctk.CTkFrame(self.main)
        self.bottom_bar.pack(pady=(20, 5))
        self.btn=ctk.CTkButton(self.bottom_bar, text=" 获取 ", command=self.worker_thread, font=('微软雅黑',14), width=120)
        self.btn.pack()

        # 右下角的 GitHub 文本链接（无按钮背景，仅下划线）
        try:
            # place inside `main` so background matches rounded container and avoids visible rectangle artifacts
            main_bg = self.main.cget('fg_color') if self.main.cget('fg_color') is not None else None
            self.github_label = ctk.CTkLabel(self.main, text='GitHub', text_color="#1a73e8", fg_color=main_bg, font=('微软雅黑',14,'underline'))
            self.github_label.place(relx=0.98, rely=0.98, anchor="se")
            self.github_label.bind("<Button-1>", lambda e: self.openweb())
        except Exception:
            # fallback to a simple tkinter label if CTkLabel fails for any reason
            import tkinter as tk
            try:
                bg = self.main.cget('fg_color') or self.root.cget('bg')
            except Exception:
                bg = self.root.cget('bg')
            self.github_label = tk.Label(self.main, text="GitHub", fg="#1a73e8", bg=bg, cursor="hand2", font=('微软雅黑',14,'underline'))
            self.github_label.place(relx=0.98, rely=0.98, anchor="se")
            self.github_label.bind("<Button-1>", lambda e: self.openweb())


    # 按钮点击触发这个方法
    def worker_thread(self):
        # 禁用按钮，防止重复点击
        self.btn.configure(state="disabled")
        self.resultBar.configure(text="工作中...")
        self.progressBar.pack(fill="x")
        self.progressBar.configure(mode="indeterminate")
        self.progressBar.start()
        # 创建一个新线程，目标函数是 self.run_heavy_task
        # daemon=True 表示如果主程序关闭，这个线程也会随之强行关闭
        thread = threading.Thread(target=self.run_heavy_task, daemon=True)
        thread.start()

    # 这个方法在【后台线程】运行
    def run_heavy_task(self):
        try:
            if data1.get()=='' or data2.get()=='' or data3.get()=='':
                error_msg="未正确填写信息"
                self.root.after(0, self.on_error, error_msg)
            else:
                username=data1.get()
                password=data2.get()
                first_monday=data3.get()
                XNXQDM=data4.get()
                calendar, data_hash=register(username, password, first_monday, XNXQDM)
                try:
                # 保存文件
                    calendar.save_as_ics_file()
                    print("文件已保存")
                    # 任务完成，通知主线程更新 UI
                    self.root.after(0, self.on_success())
                except Exception as ee:
                    print("保存失败")
                    self.root.after(0, self.on_error, str(ee))                
        except Exception as e:
            # 捕获所有未预期的异常，防止程序崩溃
            # 注意：不能在这里直接 self.label.configure(...)
            # 必须用 self.root.after(0, ...)
            self.root.after(0, self.on_error, str(e))
            

    # 回到【主线程】运行
    def on_success(self):
        self.progressBar.configure(mode="determinate")
        self.progressBar.set(1)
        self.progressBar.stop()
        self.resultBar.configure(text="文件已保存")
        self.btn.configure(state="normal") # 恢复按钮

    def on_error(self, error_msg):
        self.progressBar.configure(mode="determinate")
        self.progressBar.set(0)
        self.progressBar.stop()
        tkinter.messagebox.showerror('错误', error_msg)
        self.resultBar.configure(text="错误")
        self.btn.configure(state="normal") # 恢复按钮

    def openweb(self):
        webbrowser.open("https://github.com/Neighbor-Z/nbu-course-table-to-ics-local/")


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()

