import argparse

def launch_cli(vpn: bool):
    from login_cli import cli
    cli(vpn)

def launch_ctk(vpn: bool):
    try:
        import tkinter.messagebox
        import customtkinter as ctk
    except ImportError:
        print("CustomTkinter/Tkinter does NOT work. Use CLI instead.")
        launch_cli(vpn)
    else:
        root = ctk.CTk()
        from LoginForm import App
        app = App(root, vpn)
        root.mainloop()

def launch_pyqt6(vpn: bool):
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("PyQt6 does NOT work. Trying CustomTkinter...")
        try:
            launch_ctk(vpn)
        except Exception as e:
            print(str(e))
    else:
        import sys
        from LoginForm_pyqt import LoginWindow
        app = QApplication(sys.argv)
        win = LoginWindow(vpn)
        win.show()
        sys.exit(app.exec())

def main():
    parser = argparse.ArgumentParser(description="NBU Class Table Tool")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pyqt6", action="store_true", help="Launch the tool by using PyQt6 GUI")
    group.add_argument("--ctk", action="store_true", help="Launch the tool by using CustomTkinter GUI")
    group.add_argument("--cli", action="store_true", help="Launch the tool by using CLI")
    parser.add_argument('--no-vpn', action='store_true', help='Disable WebVPN proxy mode')

    args = parser.parse_args()

    use_vpn=not args.no_vpn

    if args.ctk:
        launch_ctk(use_vpn)
    elif args.cli:
        launch_cli(use_vpn)
    else:
        launch_pyqt6(use_vpn)

if __name__ == "__main__":
    main()

