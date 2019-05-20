import requests
import re
import js2py
import json


class Baidu:
    def __init__(self, query_str):
        self.query_str = query_str
        # 百度翻译首页
        self.url1 = "https://fanyi.baidu.com/"
        # 百度语言检测接口
        self.url2 = "https://fanyi.baidu.com/langdetect"
        # 百度翻译返回数据接口
        self.url3 = "https://fanyi.baidu.com/v2transapi"
        # 实例化session发送请求,携带百度后台返回的cookie访问后续接口地址
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36"
        }
        # 经过抓包分析,首先必须先访问一次百度翻译首页,在点击翻译按钮后浏览器会再次访问首页,返回有效的token字段
        self.session.get(self.url1)

    def get_token(self):
        response = self.session.get(self.url1)
        # 正则匹配网页返回的token字段
        token = re.findall(r"token: '(.*?)'", response.content.decode())[0]
        return token

    def get_sign(self):
        # 从本地文件打开百度的js代码片段,通过python执行js代码,解密sign加密字段
        with open("baidu.js", "r", encoding="utf-8")as f:
            text = js2py.eval_js(f.read())
            sign = text(self.query_str)
            return sign

    def get_from_to(self):
        data = {
            "query": self.query_str
        }
        response = self.session.post(self.url2, data=data)
        fromlang = json.loads(response.content.decode())["lan"]
        # 通过百度语言检测接口来确定翻译的语言类型
        to = "en" if fromlang == "zh" else "zh"
        return fromlang, to

    def get_result(self, data):
        response = self.session.post(self.url3, data=data)
        result = json.loads(response.content.decode())["trans_result"]["data"][0]["dst"]
        return result

    def run(self):
        # 获取token字段
        token = self.get_token()
        # 获取sign加密字段
        sign = self.get_sign()
        # 获取from,to字段
        fromlang, to = self.get_from_to()
        # 准备需要发送post请求接口数据
        data = {
            "from": fromlang,
            "to": to,
            "query": self.query_str,
            "transtype": "translang",
            "simple_means_flag": "3",
            "sign": sign,
            "token": token
        }
        # 向翻译接口发起请求,获取翻译的结果
        result = self.get_result(data)
        print(result)


if __name__ == '__main__':
    bd = Baidu("李信到此一游")
    bd.run()
