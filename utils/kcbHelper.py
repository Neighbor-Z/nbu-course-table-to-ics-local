import requests
import bs4
from Crypto.Cipher import AES
import base64
import time
import json
import random
import hashlib
from datetime import datetime, timezone, timedelta

url = 'https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F' \
      '%2Fehall.nbu.edu.cn%2Fnew%2Findex.html'


class AESCipher:
    def __init__(self, key):
        if len(key) != 16:
            raise RuntimeError('The length of key is less than 16.')
        self.key = key.encode()
        self.length = AES.block_size
        self.base_str = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'

    def getRndStr(self, num):
        str = ''
        for i in range(0, num):
            str = str + self.base_str[random.randint(0, 47)]
        return str

    def PKCS5Padding(self, plain_text):
        padding = self.length - len(plain_text) % self.length
        str = plain_text + padding * chr(padding)
        b_str = str.encode()
        return b_str

    def aes_encrypt(self, plain_text):
        encryptor = AES.new(self.key, AES.MODE_CBC, iv=bytes(self.getRndStr(16).encode()))
        encrypt_str = encryptor.encrypt(self.PKCS5Padding(self.getRndStr(64) + plain_text))
        return base64.b64encode(encrypt_str).decode()

    def aes_decrypt(self, cipher_text):
        decryptor = AES.new(self.key, AES.MODE_CBC, iv=bytes(self.getRndStr(16).encode()))
        plain_text = base64.decodebytes(cipher_text.encode())
        decrypt_text = decryptor.decrypt(plain_text)
        str = decrypt_text[64:-ord(decrypt_text[len(decrypt_text) - 1:])]
        return str


def getData(res, username, password):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    def find_input_value(*keys):
        for k in keys:
            el = soup.find('input', id=k) or soup.find('input', attrs={'name': k})
            if el and el.get('value') is not None:
                return el.get('value')
        return None

    # 新字段匹配（多候选名，兼容页面更新）
    pwdSalt = find_input_value('pwdDefaultEncryptSalt', 'pwdEncryptSalt', 'pwdSalt')
    if not pwdSalt:
        # open("debug_s1.html", "w", encoding="utf-8").write(res.text)
        raise RuntimeError("找不到密码 salt（pwdEncryptSalt），请联系开发者")

    crypto = AESCipher(pwdSalt)
    cipher_pwd = crypto.aes_encrypt(password)

    lt = find_input_value('lt', 'lt1') or ''
    dllt = find_input_value('dllt', 'cllt', 'loginType') or ''
    execution = find_input_value('execution') or ''
    rmShown = find_input_value('rmShown', 'rememberMe', 'remember') or '0'
    eventId = find_input_value('_eventId', 'eventId') or 'submit'

    data = {
        'username': username,
        'password': cipher_pwd,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        'rmShown': rmShown,
        '_eventId': eventId
    }
    return data


def defaultHeader():
    data = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://uis.nbu.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/605.1.15 Edg/140.0.6367.49",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    return data


def s2Header():
    data = {
        'Host': 'uis.nbu.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': '276',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="140", "Chromium";v="140", ";Not A Brand";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'MAC_OS_X',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://uis.nbu.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nbu.edu.cn%2Fnew%2Findex.html',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    return data


def indexHeader():
    data = {
        'Host': 'ehall.nbu.edu.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'https://ehall.nbu.edu.cn/publicapp/sys/myyktzd/mobile/oneCard/index.html?v=1.0&v=' + str(
            int(round(time.time() * 1000))),
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'sec-ch-ua': '"Google Chrome";v="140", "Chromium";v="140", ";Not A Brand";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Mac_OS_X',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    return data


def getCookie(username, password):
    url = "https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nbu.edu.cn%2Fnew%2Findex.html"
    session = requests.session()
    # session 1:
    s1res1 = session.get(url, headers=defaultHeader())
    # session 2
    s2res1 = session.post(url, data=getData(s1res1, username, password), headers=s2Header(), allow_redirects=False)
    # print(s2res1.text)
    if '您提供的用户名或者密码有误' in s2res1.text:
        raise ValueError('帐号或密码错误')

    time.sleep(1)

    # s2url2 = s2res1.headers.get('Location')
    # if not s2url2:
    #     raise RuntimeError("登录失败：No_s2_redirection_header ，请联系开发者")
    # s2res2 = session.get(s2url2, headers=defaultHeader(), allow_redirects=False)
    # time.sleep(2)
    # s2url3 = s2res2.headers.get('Location')
    # s2res3 = session.get(s2url3, headers=defaultHeader(), allow_redirects=False)
    # s2url4 = s2res3.headers.get('Location')
    # s2res4 = session.get(s2url4, headers=defaultHeader(), allow_redirects=False)
    # time.sleep(1)
    # s2url5 = s2res4.headers.get('Location')
    # s2res5 = session.get(s2url5, headers=indexHeader())
    
    # print(s2res5.text)
    # s2url6 = s2res5.headers.get('Location')
    # s2res6 = session.get(s2url6, headers=indexHeader())

    # 旧代码直接取 headers 会抛 KeyError
    # 新：安全的循环重定向处理
    from urllib.parse import urljoin
    
    location = s2res1.headers.get('Location') or s2res1.headers.get('location')
    if not location:
        # open("debug_s2_login.html", "w", encoding="utf-8").write(s2res1.text)
        # print("登录状态码:", s2res1.status_code)
        # print("响应头keys:", list(s2res1.headers.keys()))
        raise RuntimeError("登录失败：No_s2_redirection_header ，请联系开发者")
    
    resp = s2res1
    for i in range(5):  # 最多5次重定向
        loc = resp.headers.get('Location') or resp.headers.get('location')
        if not loc:
            break
        next_url = urljoin(resp.url, loc)
        headers = indexHeader() if i == 4 else defaultHeader()  # 最后一次用 indexHeader
        resp = session.get(next_url, headers=headers, allow_redirects=False)
        time.sleep(1 if i < 2 else 2)  # 前两次sleep 1秒，后面sleep 2秒
    return session


def renewKcbCookie(session):
    # print(session.cookies)
    rn1re1 = session.get('https://ehall.nbu.edu.cn/appShow?appId=4770397878132218', headers=indexHeader())
    # print(rn1re1.text)
    return session


def renewKcbCookieYjs(session):
    rn1re1 = session.get('https://ehall.nbu.edu.cn/appShow?appId=4979568947762216', headers=indexHeader())
    return session


def checkStudentKind(usr, pwd):
    print("{}:正在登录ehall，请等待...".format(usr))
    session = getCookie(usr, pwd)
    print("ehall登录成功")
    time.sleep(1)
    # res = session.get('https://ehall.nbu.edu.cn/jsonp/userDesktopInfo.json', headers=indexHeader())
    # info = json.loads(res.text)
    # if len(info['userId']) == 10:
    #     return 'YJS', session
    # else:
    #     return 'BKS', session
    return session


def getClassListBks(session,XNXQDM):
    print("本科生：正在尝试请求查询课程表凭证，请等待...")
    time.sleep(1)
    nsession = renewKcbCookie(session)
    kcburl = 'https://ehall.nbu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do'
    time.sleep(1)
    rn2re2 = nsession.post(kcburl, headers=indexHeader(), data={'XNXQDM': XNXQDM })
    return json.loads(rn2re2.text), hashlib.md5(
        json.dumps(json.loads(rn2re2.text)['datas']['xskcb']['rows']).encode())


def getClassListYjs(session,XNXQDM):
    # print("{}-{}:正在登录ehall，请等待...".format(usr, pwd))
    # session = getCookie(usr, pwd)
    print("研究生：正在尝试请求查询课程表凭证，请等待...")
    time.sleep(1)
    session = renewKcbCookieYjs(session)
    kcburl = 'https://ehall.nbu.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/xspkjgcx.do'
    stuInfoUrl = 'https://ehall.nbu.edu.cn/gsapp/sys/wdkbapp/wdkcb/initXsxx.do?XH='
    time.sleep(1)
    rn2re2 = session.post(kcburl, headers=indexHeader(), data={'XNXQDM': XNXQDM })
    rn2re3 = session.get(stuInfoUrl, headers=indexHeader())
    return json.loads(rn2re2.text), json.loads(rn2re3.text), hashlib.md5(rn2re2.text.encode())

'''
if __name__ == '__main__':
    user = input("请输入学号：")
    bks_or_yjs = 0 if len(user) == 9 else 1
    passwd = input("请输入密码：")
    if bks_or_yjs == 0:
        print(getClassListBks(user, passwd))
    else:
        print(getClassListYjs(user, passwd))
'''


