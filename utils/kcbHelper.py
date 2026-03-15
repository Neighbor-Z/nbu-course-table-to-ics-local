import requests
import bs4
from Crypto.Cipher import AES
import base64
import time
import json
import random
import hashlib

# WebVPN support
# WebVPN gateway URL
VPN_GATEWAY = "vpn.nbu.edu.cn:8118"

def to_vpn_url(url: str) -> str:
    """将直连内网 URL 转换为 WebVPN 代理 URL。
    规则：
      https://uis.nbu.edu.cn/path  ->  http://uis-nbu-edu-cn-s.vpn.nbu.edu.cn:8118/path
      https://ehall.nbu.edu.cn/path ->  http://ehall-nbu-edu-cn-s.vpn.nbu.edu.cn:8118/path
    即：将 scheme 改为 http，把原始域名的点换成横线，后缀 -s.vpn.nbu.edu.cn:8118
    """
    from urllib.parse import urlparse, urlunparse
    parsed = urlparse(url)
    # 原域名 "uis.nbu.edu.cn" -> "uis-nbu-edu-cn"
    vpn_host = parsed.hostname.replace('.', '-') + '-s.' + VPN_GATEWAY
    # 端口（如果原URL有显式端口则保留在新host中，否则忽略）
    new_netloc = vpn_host  # VPN_GATEWAY 已经包含端口
    new_url = urlunparse(('http', new_netloc, parsed.path, parsed.params, parsed.query, parsed.fragment))
    return new_url


# 模块级 VPN 开关（由外部在登录前设置）
_use_vpn: bool = False

def set_use_vpn(flag: bool):
    global _use_vpn
    _use_vpn = flag

def u(url: str) -> str:
    # Return URL based on current VPN state
    return to_vpn_url(url) if _use_vpn else url


# Original URLs
_LOGIN_URL        = 'https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nbu.edu.cn%2Fnew%2Findex.html'
_EHALL_BKS_APP    = 'https://ehall.nbu.edu.cn/appShow?appId=4770397878132218'
_EHALL_YJS_APP    = 'https://ehall.nbu.edu.cn/appShow?appId=4979568947762216'
_EHALL_KCB_BKS    = 'https://ehall.nbu.edu.cn/jwapp/sys/wdkb/modules/xskcb/xskcb.do'
_EHALL_KCB_YJS    = 'https://ehall.nbu.edu.cn/gsapp/sys/wdkbapp/modules/xskcb/xspkjgcx.do'
_EHALL_STU_INFO   = 'https://ehall.nbu.edu.cn/gsapp/sys/wdkbapp/wdkcb/initXsxx.do?XH='


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
    origin = 'http://uis-nbu-edu-cn-s.vpn.nbu.edu.cn:8118' if _use_vpn else 'https://uis.nbu.edu.cn'
    data = {
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        "Origin": origin,
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/605.1.15 Edg/140.0.6367.49",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    return data


def s2Header():
    if _use_vpn:
        host    = 'uis-nbu-edu-cn-s.vpn.nbu.edu.cn'
        origin  = 'http://uis-nbu-edu-cn-s.vpn.nbu.edu.cn:8118'
        referer = u('https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nbu.edu.cn%2Fnew%2Findex.html')
    else:
        host    = 'uis.nbu.edu.cn'
        origin  = 'https://uis.nbu.edu.cn'
        referer = 'https://uis.nbu.edu.cn/authserver/login?service=http%3A%2F%2Fehall.nbu.edu.cn%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.nbu.edu.cn%2Fnew%2Findex.html'
    data = {
        'Host': host,
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '"Google Chrome";v="140", "Chromium";v="140", ";Not A Brand";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'MAC_OS_X',
        'Upgrade-Insecure-Requests': '1',
        'Origin': origin,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/605.1.15',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': referer,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    return data


def indexHeader():
    if _use_vpn:
        host    = 'ehall-nbu-edu-cn-s.vpn.nbu.edu.cn'
        referer = u('https://ehall.nbu.edu.cn/publicapp/sys/myyktzd/mobile/oneCard/index.html?v=1.0&v=') + str(int(round(time.time() * 1000)))
    else:
        host    = 'ehall.nbu.edu.cn'
        referer = 'https://ehall.nbu.edu.cn/publicapp/sys/myyktzd/mobile/oneCard/index.html?v=1.0&v=' + str(int(round(time.time() * 1000)))
    data = {
        'Host': host,
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.6367.49 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': referer,
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
    login_url = u(_LOGIN_URL)
    session = requests.session()
    # session 1:
    s1res1 = session.get(login_url, headers=defaultHeader())
    # session 2
    s2res1 = session.post(login_url, data=getData(s1res1, username, password), headers=s2Header(), allow_redirects=False)
    # print(s2res1.text)
    if '您提供的用户名或者密码有误' in s2res1.text:
        raise ValueError('帐号或密码错误')

    time.sleep(1)

    # 安全的循环重定向处理
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
        # VPN 模式：将重定向 URL 也转换为 VPN 地址
        if _use_vpn:
            from urllib.parse import urlparse
            parsed = urlparse(next_url)
            # 只转换内网域名（nbu.edu.cn 结尾）
            if parsed.hostname and parsed.hostname.endswith('nbu.edu.cn') and 'vpn.nbu.edu.cn' not in parsed.hostname:
                next_url = to_vpn_url(next_url)
        headers = indexHeader() if i == 4 else defaultHeader()  # 最后一次用 indexHeader
        resp = session.get(next_url, headers=headers, allow_redirects=False)
        time.sleep(1 if i < 2 else 2)  # 前两次sleep 1秒，后面sleep 2秒
    return session


def renewKcbCookie(session):
    # print(session.cookies)
    rn1re1 = session.get(u(_EHALL_BKS_APP), headers=indexHeader())
    # print(rn1re1.text)
    return session


def renewKcbCookieYjs(session):
    rn1re1 = session.get(u(_EHALL_YJS_APP), headers=indexHeader())
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
    kcburl = u(_EHALL_KCB_BKS)
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
    kcburl   = u(_EHALL_KCB_YJS)
    stuInfoUrl = u(_EHALL_STU_INFO)
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


