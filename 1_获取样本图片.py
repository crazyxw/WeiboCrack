# -*- coding: utf-8 -*-
import io
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image


class Weibo(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = "18707329715"
        self.passwd = "ppt6923"

    def login(self):
        self.browser.get("https://passport.weibo.cn/signin/login?refer=https://m.weibo.cn")
        time.sleep(2)
        user = self.wait.until(EC.presence_of_element_located((By.ID, "loginName")))
        user.clear()
        user.send_keys(self.username)
        passwd = self.wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))
        passwd.clear()
        passwd.send_keys(self.passwd)
        passwd.send_keys(Keys.ENTER)

    def get_screenshot(self):
        """
        获取网页截图
        :return:
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(io.BytesIO(screenshot))
        return screenshot

    def get_position(self):
        """
        获取验证码位置
        :return:
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'patt-shadow')))
        time.sleep(2)  # 适当延迟,避免截图过早
        size = img.size  # 图片大小
        location = img.location  # 图片在网页中的位置
        top, buttom, left, right = location["y"], location["y"]+size["height"],location["x"],location["x"]+size["width"]
        return top, buttom, left, right

    def get_image(self):
        """
        获取验证码图片
        :return:
        """
        # 获取验证码图片位置
        top, buttom, left, right = self.get_position()
        # 获取网页截图
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, buttom))
        return captcha

    def run(self):
        count = 20
        while count:
            self.login()
            captcha = self.get_image()
            captcha.save(str(count)+".png")
            count -= 1


if __name__ == "__main__":
    weibo = Weibo()
    weibo.run()
