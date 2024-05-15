# -*- coding:utf-8 -*-
# @time:2020-9-16 11:06
# POWERD BY:ECHO
import os
import time

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

caps = {
                      "platformName": "Android",
                      "platformVersion": "10",
                      "deviceName": "6HJ4C20110006671",
                      "appPackage": "com.evergrande.bao.consumer",
                      "appActivity": ".splash.SplashActivity",
                      "noReset": True,
                      "unicodeKeyboard": True,
                      "resetKeyboard": True,
                      "automationName": "UiAutomator1"
                    }

driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", caps)
driver.implicitly_wait(10)

el1 = driver.find_element_by_id("com.evergrande.bao.consumer:id/img_close")
el1.click()
el2 = driver.find_element_by_xpath(
    "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView")
el2.click()
el3 = driver.find_element_by_id("com.evergrande.bao.consumer:id/search_edit_view")
el3.send_keys("北京")

cmd = r"adb shell ime set com.sohu.inputmethod.sogou/.SogouIME" #adb shell ime list -s
os.system(cmd)
# cmd = r"adb shell input keyevent 84 "
# os.popen(cmd).read()
driver.keyevent(66)

# print("执行keyevent")
#TouchAction(driver).tap(x=1006, y=2187).perform()

time.sleep(3)


TouchAction(driver).press(x=540, y=1944).move_to(x=540, y=500).release().perform()



