
def cli():
    import getpass
    print("宁波大学课表工具 v1.5.2 CLI\n")
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
            calendar, data_hash=register(username, password, first_monday, XNXQDM)
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