#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.support import expected_conditions as EC # 等待操作需要导入的库
from selenium.webdriver.common.action_chains import ActionChains # 用于完成一系列操作
from selenium.webdriver.support.wait import WebDriverWait # 等待某个特定的操作
from selenium.webdriver.chrome.options import Options # 设置参数
from selenium.webdriver.support.select import Select # 专门用于处理下拉框
from selenium.webdriver.common.keys import Keys # 所有按键的指令
from selenium.webdriver.common.by import By # 指定搜索方法
import time
import base64
import json
import requests

PHONE = "你的长江雨课堂手机号"
PASSWORD = "你的长江雨课堂密码"

TJ_ACCOUNT = '你的图鉴账号'
TJ_PASSWORD = '你的图鉴密码'

# 图鉴
def base64_api(uname, pwd, img, typeid):
    """
    图鉴自带的类，调用即可
    """
    if(type(img) == type("str")): # 传入图片路径
        with open(img, 'rb') as f:
            base64_data = base64.b64encode(f.read())
            b64 = base64_data.decode()
    else: # 传入图片字节
        base64_data = base64.b64encode(img)
        b64 = base64_data.decode()
    data = {"username": uname, "password": pwd, "typeid": typeid, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/predict", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]

# 内核驱动参数
options = Options()
# 处理 SSL 证书错误问题、隐藏自动化操作、忽略无用的日志、禁用 GPU（默认添加）
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
options.add_argument('--disable-gpu')
# 无头浏览器，窗口调大，防止样式堆叠
#options.add_argument("--headless")
#options.add_argument("--window-size=4000,1600")

# 初始化
web = Chrome(options=options)
# 进入网站
web.get("https://changjiang.yuketang.cn/web")
# 全局隐式等待 5 秒，即获取元素的函数超过 5 秒就报错超时
web.implicitly_wait(5)

def login(web: Chrome):
    # 刷新页面
    web.refresh()
    # 切换账号登入
    element = web.find_element(By.XPATH, "//div[@class='mabox mabox_thu toggle-box']/img")
    element.click()
    # 输入手机号和密码
    element = web.find_element(By.XPATH, "//div[@class='account-box toggle-box']//input[@type='mobile']")
    element.send_keys(PHONE)
    element = web.find_element(By.XPATH, "//div[@class='account-box toggle-box']//input[@type='password']")
    element.send_keys(PASSWORD)
    # 点击登入
    element = web.find_element(By.XPATH, "//div[@class='submit-btn login-btn customMargin']")
    element.click()
    # 切换到验证码的 iframe 中
    iframe = web.find_element(By.XPATH, "//iframe[@class='tcaptcha-iframe']")
    web.switch_to.frame(iframe)
    # 绕过滑块（识别滑块坐标，并滑动滑块）
    img = web.find_element(By.XPATH, "//div[@class='tc-captcha-mobile tc-slide']") # 读取网络图片，标签为 img
    bs = img.screenshot_as_png # 截图，获得图片字节
    result = base64_api(uname=TJ_ACCOUNT, pwd=TJ_PASSWORD, img=bs, typeid=33) # 图鉴识别
    move = int(result) - 47.5 # 需要移动的距离减去滑块距离左边边框的位置，从而得到实际需要移动的距离
    button = web.find_element(By.ID, 'tcaptcha_drag_button')
    ac = ActionChains(web)
    ac.click_and_hold(button)
    ac.move_by_offset(xoffset=move, yoffset=0)
    ac.pause(3)
    ac.move_to_element(button) # 鼠标悬浮在滑块上，才能触发释放滑块的功能
    ac.release()
    ac.perform()
    # 切换回到上层 iframe
    web.switch_to.parent_frame()
    # 强制等待 10 秒，进入登入界面
    time.sleep(10)
    return web, web.title

def register(web: Chrome):
    # 刷新页面
    web.refresh()
    # 验证登入时效未过期
    if(web.title != "雨课堂"): return False
    # 点击课程
    try:
        element = web.find_element(By.XPATH, "//div[@class='onlesson']")
        element.click()
        class_name = web.find_element(By.XPATH, "//div[@class='onlessonlist']/div/div[1]/p").text
        print(class_name + "成功打卡！！")
        element = web.find_element(By.XPATH, "//div[@class='onlessonlist']/div/div[2]")
        element.click()
        time.sleep(10)
        # 删除新增加的页面
        web.switch_to.window(web.window_handles[-1])
        web.close()
        web.switch_to.window(web.window_handles[0])
    except:
        print("当前没有课程")
    return True

if __name__=="__main__":
    """
    每天上午开始 10 点开始执行，直到晚上 16 点关闭
    每半个小时检查一次，共检查 12 次
    """
    for i in range(10): # 最多允许失败 10 次
        web, title = login(web)
        if title == "雨课堂" : break # 验证登入成功
    # 半个小时一次检查
    for i in range(12):
        result = register(web)
        while(result == False): # 以防登入时效过期
            web, title = login(web)
            result = register(web)
        time.sleep(30 * 60)
    # 关闭整个驱动
    web.quit()
