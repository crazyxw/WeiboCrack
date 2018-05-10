# -*- coding: utf-8 -*-
import io
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from PIL import Image
import numpy as np
from ims import ims


class WeiboLogin(object):
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = "13974524141"
        self.passwd = "ppt9871"

    def login(self):
        """
        登陆
        :return:
        """
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

    def img_to_array(self, im):
        im = im.convert("L")
        data = im.getdata()
        data = np.matrix(data)
        # 把data封装成字典
        data = data.tolist()
        return data

    def contrast_two_img(self, data1, data2):
        """
        比较两个数组是否相似
        :param data1:
        :param data2:
        :return:
        """
        is_xt = True
        for i in range(len(data1[0])):
            if abs(data1[0][i] - data2[0][i]) > 10:
                is_xt = False
                break
        return is_xt

    def contrast(self, captcha):
        """
        匹配图片
        :return: 拖动顺序
        """
        # 图片转矩阵
        data = self.img_to_array(captcha)
        is_xt = ""
        for i in ims:
            for k, j in i.items():
                if self.contrast_two_img(data, j):
                    is_xt = k
                    break
        return is_xt

    def move(self, order):
        time.sleep(2)
        dots = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "patt-dots")))
        elements = [dots[int(i)-1] for i in order]  # 给获取到的四个点排序
        times = 50
        for i in range(4):
            if i != 0:
                x, y = elements[i].location["x"]-elements[i-1].location["x"], elements[i].location["y"]-elements[i-1].location["y"]
                for k in range(times):
                    ActionChains(self.browser).move_by_offset(xoffset=x/times, yoffset=y/times).perform()
            else:
                ActionChains(self.browser).move_to_element(elements[i]).click_and_hold().perform()
        ActionChains(self.browser).release().perform()
        time.sleep(3)

    def run(self):
        # 登陆
        self.login()
        # 获取验证码对象
        captcha = self.get_image()
        # 获取匹配出来的拖动顺序
        order = self.contrast(captcha)
        print("拖动顺序:", order)
        # 按顺序拖动
        self.move(order)


if __name__ == "__main__":
    weibo = WeiboLogin()
    weibo.run()

