import json
import os
import time
import pickle

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


class Concert(object):
    def __init__(self):
        with open("info.json", "r") as f:
            config_json = f.read()
            config = json.loads(config_json)
            print("Load config success!")

        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=options)
        f = open("stealth.min.js", mode="r", encoding="utf8").read()
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": f})

        self.url = config["url"]
        self.login_url = config["login_url"]
        self.ticket_num = config["ticket_num"]
        self.ticket_url = config["ticket_url"]
        self.login_method = config["login_method"]
        self.phone = config["phone"]
        self.pwd = config["pwd"]

    def do(self):
        self.driver.get(self.login_url)
        self.driver.maximize_window()
        self.driver.switch_to.frame(0)
        self.driver.find_element(by=By.XPATH, value="//*[@id=\"fm-login-id\"]").send_keys(self.phone)
        self.driver.find_element(by=By.XPATH, value="//*[@id=\"fm-login-password\"]").send_keys(self.pwd)
        self.driver.find_element(by=By.XPATH, value="//*[@id=\"login-form\"]/div[4]/button").click()

        time.sleep(3)
        if self.element_exist("//*[@id=\"J_GetCode\"]"):
            self.driver.find_element(by=By.XPATH, value="//*[@id=\"J_GetCode\"]").click()
            input_code = input("验证码：")

            self.driver.find_element(by=By.XPATH, value="//*[@id=\"J_Checkcode\"]").send_keys(input_code)
            self.driver.find_element(by=By.XPATH, value="//*[@id=\"btn-submit\"]").click()
            time.sleep(3)

        self.driver.get(self.ticket_url)
        while True:
            if self.element_exist("/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[4]/div[7]/div/div[3]/div[3]"):
                buy_element = self.driver.find_element(by=By.XPATH, value="/html/body/div[2]/div/div[1]/div[1]/div/div[2]/div[4]/div[7]/div/div[3]/div[3]")
                if buy_element.text == "不，立即购买":
                    buy_element.click()

                elif buy_element.text == "不，选座购买":
                    buy_element.click()
                    # 选第一个元素，第二个是套票
                    price_list_first = self.driver.find_element(by=By.CSS_SELECTOR, value=".price-list__item:first-child")
                    price_divs = price_list_first.find_elements(by=By.TAG_NAME, value="div")

                    # 初始化最高价格和对应的div元素
                    max_price = 0
                    max_price_div = None

                    # 遍历price元素，找到最高价格的元素
                    for price_div in price_divs:
                        try:
                            price_element = price_div.find_element(by=By.CSS_SELECTOR, value="span.price__text")
                        except Exception as e:
                            continue
                        price_text = price_element.text
                        price_value = int(price_text.replace("￥", ""))  # 去掉￥符号并转换为整数
                        if price_value > max_price:
                            max_price = price_value
                            max_price_div = price_div

                    if max_price_div is None:
                        raise Exception("Find Error")

                    max_price_div.click()
                    self.driver.find_element(by=By.XPATH, value="//*[@id=\"app\"]/div/div[4]/div[2]/button").click()
                break
            else:
                time.sleep(0.05)
                self.driver.refresh()

    def finish(self):
        self.driver.quit()

    def element_exist(self, element):
        flag = True
        browser = self.driver
        try:
            browser.find_element(by=By.XPATH, value=element)
            return flag
        except:
            flag = False
            return flag


if __name__ == '__main__':
    try:
        impl = Concert()
        impl.do()
        time.sleep(180)
    except Exception as e:
        print(e)
