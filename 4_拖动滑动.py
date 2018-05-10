# -*- coding: utf-8 -*-

import io
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome()
wait = WebDriverWait(browser, 20)
username = "18707329715"
password = "ppt6923"


def login():
    browser.get("https://passport.weibo.cn/signin/login?refer=https://m.weibo.cn")
    time.sleep(2)
    user = wait.until(EC.presence_of_element_located((By.ID, "loginName")))
    user.clear()
    user.send_keys(username)
    passwd = wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))
    passwd.clear()
    passwd.send_keys(password)
    passwd.send_keys(Keys.ENTER)


def move():
    order = "3214"
    dots = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "patt-dots")))
    elements = [dots[int(i) - 1] for i in order]  # 给获取到的四个点排序
    times = 50
    for i in range(4):
        if i != 0:
            x, y = elements[i].location["x"] - elements[i - 1].location["x"], elements[i].location["y"] - \
                   elements[i - 1].location["y"]
            for k in range(times):
                ActionChains(browser).move_by_offset(xoffset=x / times, yoffset=y / times).perform()
        else:
            ActionChains(browser).move_to_element(elements[i]).click_and_hold().perform()
    ActionChains(browser).release().perform()

login()
time.sleep(5)
move()
