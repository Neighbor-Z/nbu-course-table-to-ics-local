from __version__ import (
    __build__,
    __version__,
)

def cli(use_vpn: bool):
    import getpass
    print(f"宁波大学课表工具 v{__version__} CLI\n")
    try:
        import readline
    except Exception as e:
        pass
    username = input("请输入学号: ")
    password = getpass.getpass("请输入密码: (不显示)") 
    first_monday = input("请输入首个周一: (默认值:2026-03-02)")
    if first_monday=='':
        first_monday = "2026-03-02"
    XNXQDM = input("请输入学期: (默认值:2025-2026-2)")
    if XNXQDM=='':
        XNXQDM = "2025-2026-2"

    try:
        if username=='' or password=='':
            error_msg="未正确填写信息"
            print(error_msg)
        else:
            from app.index import register
            calendar, session=register(username, password, first_monday, XNXQDM, None, use_vpn)
            try:
                calendar.save_as_ics_file()
                print("文件已保存")
            except Exception as ee:
                print("保存失败")
                print(str(ee))                
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    cli()