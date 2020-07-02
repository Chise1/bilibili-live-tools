import rsa

from Service import User
from bilibili import bilibili
from printer import Printer
import base64
import requests
from urllib import parse

# temporary app parameter
appkey = '4409e2ce8ffd12b8'
build = '101800'
# device = 'android_tv_yst'
mobi_app = 'android_tv_yst'
app_secret = '59b43e04ad6965f34319062b478f83dd'


class login():
    auto_captcha_times = 3

    def normal_login(self, username, password):
        # url = 'https://passport.bilibili.com/api/oauth2/login'   #旧接口
        # url = "https://passport.snm0516.aisee.tv/api/tv/login"
        url = "https://passport.bilibili.com/api/v3/oauth2/login"

        temp_params = f"appkey={appkey}&build={build}&captcha=&channel=master&guid=XYEBAA3E54D502E17BD606F0589A356902FCF&mobi_app={mobi_app}&password={password}&platform={bilibili().dic_bilibili['platform']}&token=5598158bcd8511e1&ts=0&username={username}"
        data = f"{temp_params}&sign={bilibili().calc_sign(temp_params, app_secret)}"
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=data, headers=headers)
        return response

    def login_with_captcha(self, username, password):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'cookie': "sid=hxt5szbb"
        }
        s = requests.session()
        url = "https://passport.snm0516.aisee.tv/api/captcha?token=5598158bcd8511e1"
        res = s.get(url, headers=headers)
        tmp1 = base64.b64encode(res.content)
        for _ in range(login.auto_captcha_times):
            try:
                captcha = bilibili().cnn_captcha(tmp1)
                break
            except Exception:
                Printer().printer("验证码识别服务器连接失败", "Error", "red")
                login.auto_captcha_times -= 1
        else:
            try:
                from PIL import Image
                from io import BytesIO
                img = Image.open(BytesIO(res.content))
                img.show()
                captcha = input('输入验证码\n').strip()
            except ImportError:
                Printer().printer("安装 Pillow 库后重启，以弹出验证码图片", "Error", "red")
                exit()

        temp_params = f"appkey={appkey}&build={build}&captcha={captcha}&channel=master&guid=XYEBAA3E54D502E17BD606F0589A356902FCF&mobi_app={mobi_app}&password={password}&platform={bilibili().dic_bilibili['platform']}&token=5598158bcd8511e1&ts=0&username={username}"
        data = f"{temp_params}&sign={bilibili().calc_sign(temp_params, app_secret)}"
        headers['Content-type'] = "application/x-www-form-urlencoded"
        headers['cookie'] = "sid=hxt5szbb"
        url = "https://passport.snm0516.aisee.tv/api/tv/login"
        response = s.post(url, data=data, headers=headers)
        return response

    def access_token_2_cookies(self, access_token):
        params = f"access_key={access_token}&appkey={appkey}&gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fhome"
        url = f"https://passport.bilibili.com/api/login/sso?{params}&sign={bilibili().calc_sign(params, app_secret)}"
        response = requests.get(url, allow_redirects=False)
        return response.cookies.get_dict(domain=".bilibili.com")

    async def login(self):
        username = str(bilibili().dic_bilibili['account']['username'])
        password = str(bilibili().dic_bilibili['account']['password'])
        if username != "":
            while True:
                response = bilibili().request_getkey()
                value = response.json()['data']
                key = value['key']
                Hash = str(value['hash'])
                calcd_username, calcd_password = bilibili().calc_name_passw(key, Hash, username, password)
                response = self.normal_login(calcd_username, calcd_password)
                while response.json()['code'] == -105:
                    response = self.login_with_captcha(calcd_username, calcd_password)
                if response.json()['code'] == -662:  # "can't decrypt rsa password~"
                    Printer().printer("打码时间太长key失效，重试", "Error", "red")
                    continue
                break
            try:
                access_key = response.json()['data']['token_info']['access_token']
                cookie_info = self.access_token_2_cookies(access_key)
                cookie_format = ""
                for key, value in cookie_info.items():
                    cookie_format = cookie_format + key + "=" + value + ";"
                bilibili().dic_bilibili['csrf'] = cookie_info['bili_jct']
                bilibili().dic_bilibili['access_key'] = access_key
                bilibili().dic_bilibili['cookie'] = cookie_format
                bilibili().dic_bilibili['uid'] = int(cookie_info['DedeUserID'])
                bilibili().dic_bilibili['pcheaders']['cookie'] = cookie_format
                bilibili().dic_bilibili['appheaders']['cookie'] = cookie_format
                dic_saved_session = {
                    'csrf': cookie_info['bili_jct'],
                    'access_key': access_key,
                    'cookie': cookie_format,
                    'uid': cookie_info['DedeUserID']
                }
                await User().update_cookie(dic_saved_session)
                Printer().printer(f"登录成功", "Info", "green")
            except:
                Printer().printer(f"登录失败,错误信息为:{response.json()}", "Error", "red")

    async def login_new(self, ):
        if bilibili().dic_bilibili['session']['cookie']:
            Printer().printer(f"复用cookie", "Info", "green")
            bilibili().load_session(bilibili().dic_bilibili['session'])
        else:
            return self.login()

    async def login2(self,):
        username = bilibili().dic_bilibili['account']['username']
        password = bilibili().dic_bilibili['account']['password']
        json_rsp = await bilibili().fetch_key()
        data = json_rsp['data']
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(data['key'])
        crypto_password = base64.b64encode(
            rsa.encrypt((data['hash'] + password).encode('utf-8'), pubkey)
        )
        url_password = parse.quote_plus(crypto_password)
        url_name = parse.quote_plus(username)

        json_rsp = await bilibili().login_bili2(url_name, url_password)
        while json_rsp['code'] == -105:
            binary_rsp = await bilibili().fetch_capcha()
            captcha = await bilibili().cnn_captcha2( binary_rsp)
            json_rsp = await bilibili().login_bili2(url_name, url_password, captcha)

        if not json_rsp['code'] and not json_rsp['data']['status']:
            data = json_rsp['data']
            access_key = data['token_info']['access_token']
            refresh_token = data['token_info']['refresh_token']
            cookies = data['cookie_info']['cookies']
            list_cookies = [f'{i["name"]}={i["value"]}' for i in cookies]
            cookie = ';'.join(list_cookies)
            login_data = {
                'csrf': cookies[0]['value'],
                'access_key': access_key,
                'refresh_token': refresh_token,
                'cookie': cookie,
                'uid': cookies[1]['value']
            }
            await User().update_cookie(login_data)
        else:
            login_data = {
                'csrf': f'{json_rsp}',
                'access_key': '',
                'refresh_token': '',
                'cookie': '',
                'uid': 'NULL'
            }
            await User().update_cookie(login_data)
            return False