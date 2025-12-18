import sys
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QGridLayout, QHBoxLayout, QVBoxLayout, QProgressBar, QMessageBox, QFileDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from app.index import register


class Worker(QThread):
    finished = pyqtSignal(object)  # 传递日历对象
    error = pyqtSignal(str)
    status = pyqtSignal(str)
    progress = pyqtSignal(int)

    def __init__(self, username, password, first_monday, XNXQDM):
        super().__init__()
        self.username = username
        self.password = password
        self.first_monday = first_monday
        self.XNXQDM = XNXQDM
        self._captured = []

    def run(self):
        try:
            # Call existing business logic (may perform network I/O)
            # Redirect prints from register() to status signal and emit progress
            import sys
            original_stdout = sys.stdout
            self._progress_val = 0
            self._captured.clear()

            class _Redirect:
                def __init__(self, outer):
                    self.outer = outer

                def write(self, text):
                    try:
                        # accumulate all printed text so we can save it later
                        if text:
                            self.outer._captured.append(text)
                        if text and text.strip():
                            self.outer.status.emit(text.strip())
                            # bump progress conservatively
                            self.outer._progress_val += 20
                            if self.outer._progress_val > 100:
                                self.outer._progress_val = 100
                            self.outer.progress.emit(self.outer._progress_val)
                    except Exception:
                        pass

                def flush(self):
                    pass

            sys.stdout = _Redirect(self)
            try:
                calendar, data_hash = register(self.username, self.password, self.first_monday, self.XNXQDM)
                # ensure progress reaches 100 on success
                self.progress.emit(100)
                # join captured stdout and emit to main thread for saving
                captured_text = ''.join(self._captured)
                self.finished.emit(calendar)
            finally:
                sys.stdout = original_stdout
        except Exception as e:
            self.error.emit(str(e))


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("宁波大学课表工具 v1.5.2 PyQt6")
        self.setMinimumSize(520, 360)

        self._worker = None

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        # Top area: theme toggle
        top_h = QHBoxLayout()
        top_h.addStretch()
        self.theme_btn = QPushButton("Dark")
        self.theme_btn.setCheckable(True)
        self.theme_btn.setFixedWidth(120)
        # fixed height to avoid layout shift between styles
        self.theme_btn.setFixedHeight(30)
        self.theme_btn.setStyleSheet("padding:4px 8px; border-radius:6px;")
        self.theme_btn.clicked.connect(self._on_theme_toggle)
        top_h.addWidget(self.theme_btn)
        # ensure objectName is set so stylesheet targets correctly and apply initial theme
        self.theme_btn.setObjectName('theme_btn')
        self._set_dark_theme(False)
        main_layout.addLayout(top_h)

        # Form grid: left column 学号/密码, right column 学期/首个周一
        grid = QGridLayout()
        grid.setContentsMargins(12, 6, 12, 6)
        grid.setHorizontalSpacing(20)

        # Increase base font size ~50% for better readability
        base_font = QApplication.font()
        try:
            base_pt = max(10, int(base_font.pointSize() * 1.5))
        except Exception:
            base_pt = 16
        font = base_font
        font.setPointSize(base_pt)

        lbl_user = QLabel("学号")
        lbl_user.setFont(font)
        self.edit_user = QLineEdit()
        self.edit_user.setFont(font)
        self.edit_user.setPlaceholderText("请输入学号")
        self.edit_user.setFixedHeight(int(base_pt * 2.2))

        lbl_term = QLabel("学期")
        lbl_term.setFont(font)
        self.edit_term = QLineEdit()
        self.edit_term.setFont(font)
        self.edit_term.setPlaceholderText("2025-2026-1")
        self.edit_term.setText("2025-2026-1")
        self.edit_term.setFixedHeight(int(base_pt * 2.2))

        lbl_pwd = QLabel("密码")
        lbl_pwd.setFont(font)
        self.edit_pwd = QLineEdit()
        self.edit_pwd.setFont(font)
        self.edit_pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.edit_pwd.setPlaceholderText("请输入密码")
        self.edit_pwd.setFixedHeight(int(base_pt * 2.2))

        lbl_monday = QLabel("首个周一")
        lbl_monday.setFont(font)
        self.edit_monday = QLineEdit()
        self.edit_monday.setFont(font)
        self.edit_monday.setPlaceholderText("YYYY-MM-DD")
        self.edit_monday.setText("2025-09-08")
        self.edit_monday.setFixedHeight(int(base_pt * 2.2))

        grid.addWidget(lbl_user, 0, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.edit_user, 1, 0)
        grid.addWidget(lbl_pwd, 2, 0, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.edit_pwd, 3, 0)

        grid.addWidget(lbl_term, 0, 1, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.edit_term, 1, 1)
        grid.addWidget(lbl_monday, 2, 1, Qt.AlignmentFlag.AlignLeft)
        grid.addWidget(self.edit_monday, 3, 1)

        main_layout.addLayout(grid)

        # Status / progress
        self.progress = QProgressBar()
        try:
            self.progress.setTextVisible(False)
        except Exception:
            pass
        self.progress.setVisible(False)
        self.progress.setFixedHeight(int(base_pt * 0.9))
        main_layout.addWidget(self.progress)

        # Buttons area
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_fetch = QPushButton("获取")
        self.btn_fetch.setFixedWidth(180)
        btn_font = font
        btn_font.setBold(True)
        self.btn_fetch.setFont(btn_font)
        self.btn_fetch.clicked.connect(self.on_fetch)
        btn_layout.addWidget(self.btn_fetch)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Status label
        self.status_label = QLabel("")
        self.status_label.setFont(font)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # GitHub link at bottom-right
        link_label = QLabel('<a href="https://github.com/Neighbor-Z/nbu-course-table-to-ics-local/">GitHub</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        link_label.setFont(font)
        main_layout.addWidget(link_label)

        # keyboard return triggers fetch
        self.edit_user.returnPressed.connect(self.on_fetch)
        self.edit_pwd.returnPressed.connect(self.on_fetch)
        self.edit_monday.returnPressed.connect(self.on_fetch)

    def on_fetch(self):
        # Prevent duplicate requests
        if self._worker is not None and self._worker.isRunning():
            return

        username = self.edit_user.text().strip()
        password = self.edit_pwd.text().strip()
        first_monday = self.edit_monday.text().strip()
        XNXQDM = self.edit_term.text().strip()

        if not username or not password or not first_monday:
            QMessageBox.warning(self, "错误", "请完整填写学号、密码、首个周一")
            return

        # disable UI controls
        self.btn_fetch.setEnabled(False)
        self.status_label.setText("处理中...")
        # determinate progress 0-100; will be incremented from worker status
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setVisible(True)

        # start worker thread
        self._worker = Worker(username, password, first_monday, XNXQDM)
        self._worker.finished.connect(self.on_finished)
        self._worker.error.connect(self.on_error)
        self._worker.status.connect(self._on_status)
        self._worker.progress.connect(self._animate_progress)
        self._worker.start()

        # keep a local progress tracker (main-thread view)
        self._progress_value = 0

    def _animate_progress(self, value):
        # Animate the progress bar to the new value and keep a reference to avoid GC
        try:
            if hasattr(self, '_progress_anim') and self._progress_anim is not None:
                try:
                    self._progress_anim.stop()
                except Exception:
                    pass
            self._progress_anim = QPropertyAnimation(self.progress, b"value", self)
            self._progress_anim.setDuration(120)
            self._progress_anim.setStartValue(self.progress.value())
            self._progress_anim.setEndValue(int(value))
            self._progress_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            self._progress_anim.start()
        except Exception:
            # fallback to direct set if animation fails
            try:
                self.progress.setValue(int(value))
            except Exception:
                pass

    def _on_status(self, msg: str):
        # Update status label when worker emits status messages
        try:
            self.status_label.setText(msg)
        except Exception:
            pass

    def on_finished(self, calendar):
        # ensure progress shows completion
        self.progress.setRange(0, 100)
        self._animate_progress(100)
        self.progress.setVisible(True)
        # 在主线程中弹出文件保存对话框
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存课程表文件",
            f"{calendar.calendar_name}.ics",
            "ICS Files (*.ics);;All Files (*)"
        )

        if file_path:
            try:
                # 保存文件
                calendar.save_as_ics_file(file_path)
                self.status_label.setText("文件已保存")
                QMessageBox.information(self, "成功", f"文件已保存到：\n{file_path}")
            except Exception as e:
                self.status_label.setText("保存失败")
                QMessageBox.critical(self, "错误", f"保存文件时出错：{str(e)}")
        else:
            self.status_label.setText("已取消保存")
        
        # reset UI
        self.progress.setVisible(False)
        self.progress.setValue(0)
        self.btn_fetch.setEnabled(True)
        self._worker = None

    def on_error(self, msg: str):
        self.progress.setVisible(False)
        self.progress.setValue(0)
        # self.status_label.setText(f"错误: {msg}")
        self.status_label.setText("错误")
        QMessageBox.critical(self, "错误", f"发生异常：{msg}")
        self.btn_fetch.setEnabled(True)
        self._worker = None

    def _on_theme_toggle(self):
        # Toggle theme and update button text
        checked = self.theme_btn.isChecked()
        if checked:
            self._set_dark_theme(True)
            self.theme_btn.setText("Light")
        else:
            self._set_dark_theme(False)
            self.theme_btn.setText("Dark")

    def _set_dark_theme(self, dark: bool):
        # Use symmetric styles for light and dark so layout/size remain identical
        if dark:
            ss = """
            QWidget { background-color: #2b2b2b; color: #e6e6e6; }
            QLineEdit { background-color: #3c3f41; color: #ffffff; border: 1px solid #555555; padding:6px; }
            QPushButton { background-color: #3768a0; color: #ffffff; border-radius: 8px; padding:6px 12px; }
            QPushButton:disabled { background-color: #555555; color: #999999; }
            QPushButton#theme_btn { background-color: #3768a0; color: #ffffff; }
            QProgressBar { background-color: #3a3f44; color: #ffffff; border-radius:6px; height:12px; }
            QProgressBar::chunk { background-color: #58a; border-radius:6px; }
            QLabel { color: #e6e6e6; }
            """
        else:
                ss = """
                QWidget { background-color: #f3f3f3; color: #222222; }
                QLineEdit { background-color: #ffffff; color: #222222; border: 1px solid #cfcfcf; padding:6px; }
                QPushButton { background-color: #528ccb; color: #ffffff; border-radius: 8px; padding:6px 12px; }
                QPushButton:disabled { background-color: #cccccc; color: #888888; }
                /* Make theme button blue in light mode as well */
                QPushButton#theme_btn { background-color: #528ccb; color: #ffffff; }
                QProgressBar { background-color: #e9e9e9; color: #222222; border-radius:6px; height:12px; }
                QProgressBar::chunk { background-color: #2b82d9; border-radius:6px; }
                QLabel { color: #222222; }
                """
        # Apply and ensure theme button keeps consistent size; also set objectName to target it
        self.theme_btn.setObjectName('theme_btn')
        app = QApplication.instance()
        if app:
            app.setStyleSheet(ss)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    win.show()
    sys.exit(app.exec())
