import json
import os
import time
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class Concert(object):
    def __init__(self):
        with open("info.json", "r") as f:
            config_json = f.read()
            config = json.loads(config_json)
            print("Load config success!")

        self.driver = webdriver.Chrome()
        self.url = config["url"]
        self.login_url = config["login_url"]
        self.ticket_num = config["ticket_num"]
        self.ticket_url = config["ticket_url"]
        self.login_method = config["login_method"]

    def set_cookie(self):
        self.driver.get(self.url)
        print("###请点击登录###")
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:
            time.sleep(1)
        print('###请扫码登录###')
        while self.driver.title != '大麦网-全球演出赛事官方购票平台-100%正品、先付先抢、在线选座！':
            time.sleep(1)
        print("###扫码成功###")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print("###Cookie保存成功###")
        self.driver.get(self.ticket_url)

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须有，不然就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print('###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        if self.login_method == 0:
            self.driver.get(self.login_url)
            # 载入登录界面
            print('###开始登录###')

        elif self.login_method == 1:
            if not os.path.exists('cookies.pkl'):
                # 如果不存在cookie.pkl,就获取一下
                self.set_cookie()
            else:
                self.driver.get(self.target_url)
                self.get_cookie()


if __name__ == '__main__':
    concert = Concert()
    concert.set_cookie()
