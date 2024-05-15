# -*- coding:utf-8 -*-
# @time:2020-9-7 11:18
# POWERD BY:ECHO
import os
import time
import traceback

import cv2
from selenium import webdriver
from selenium.webdriver import ActionChains

from common.commonKeys import sysKey
from common.getimg import get_img, FindPic
from common.logger import logger


class WEB:
    def __init__(self,writer):
        self.writer = writer
        self.row = 0
        self.conf = {}
        self.driver = None
        self.e = None

    def openbrowser(self,browser = "chrome",exepath=""):
        """
        @param browser:打开浏览器  firefox 火狐浏览器；chrome谷歌浏览器；ie ie浏览器
        @param exepath:driver的路径
        @return:
        """
        try:
            if browser is None or browser == "chrome" or browser == "":
                option = webdriver.ChromeOptions()
                userfile = os.environ["USERPROFILE"] #获取用户文件路径
                #chrome://version查看个人资料路径
                option.add_argument(r"--user-data-dir=%s\AppData\Local\Google\Chrome\User"%userfile)
                if exepath == "":
                    exepath = "./lib/conf/chromedriver.exe"
                self.driver = webdriver.Chrome(options=option,executable_path=exepath)

            elif browser == "firefox":
                if exepath == "":
                    exepath = "./lib/conf/geckodriver.exe"
                opt = webdriver.FirefoxOptions()
                #about:support
                opt.profile = r'%s\AppData\Roaming\Mozilla\Firefox\Profiles\pza6n3te.default-release' % os.environ["USERPROFILE"]
                self.driver = webdriver.Firefox(executable_path=exepath,options=opt)
                logger.info("open firefox browser")

            elif browser == "ie":
                if exepath == "":
                    exepath = "./lib/conf/IEDriverServer.exe"

                opt = webdriver.IeOptions()
                opt.profile = r'%s\Local\Microsoft\Windows\INetCache' % os.environ["USERPROFILE"]
                self.driver = webdriver.Ie(executable_path=exepath,ie_options=opt)

            self.driver.implicitly_wait(10) #添加隐式等待
            self.driver.maximize_window()
            self.__writer_excel(True,"打开%s浏览器成功"%browser)

        except Exception as e:
            self.__writer_excel(False,traceback.format_exc())
            logger.exception(e)
            self.writer.save_close()
            exit(-1) #退出运行



    def geturl(self,url):
        """
        打开网址
        @param url: 网页地址
        @return:
        """
        if self.driver is None:
            self.__writer_excel(False,"浏览器不存在")
            return  False
        try:
            self.driver.get(url)
            self.__writer_excel(True, "访问地址%s成功"%url)
            return True
        except Exception as e:
            logger.exception(e)
            self.__writer_excel(False, "访问地址%s失败"%url)
            return False

    def click(self,locator):
        """
        通过元素定位点击
        @param locator:
        @return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False, self.e)
            return False
        try:
            ele.click()
            self.__writer_excel(True, "点击元素%s成功" % locator)
            return True
        except Exception as e:
            self.__writer_excel(False, traceback.format_exc())
            logger.exception(self.e)
            return False

    def clickhref(self,locator):
        """
        通过定位找到a标签元素，获取href链接，进行跳转，主要用于IE有可能点击失败的情况
        @param loctor:
        @return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False, self.e)
            return False

        try:
            href = ele.get_attribute('href')
            self.driver.get(href)
            self.__writer_excel(True, "链接点击成功")
            return True
        except Exception as e:
            self.__writer_excel(False, traceback.format_exc())
            return False

    def jsclick(self,locator):
        """
        点击a标签 针对selenium点击不了的情况
        触发js事件 javascript:void(0)
        @param locator:
        @return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False, self.e)
            return False
        try:
            self.driver.execute_script("$(arguments[0].click())", ele)
            self.__writer_excel(True, "点击链接成功")
            return True
        except Exception as e:
            logger.exception(self.e)
            self.__writer_excel(False, traceback.format_exc())
            return False

    def runjs(self, js):
        """
        点击a标签触发js事件 JavaScript:void(0);
        :param js:
        :return:
        """
        try:
            time.sleep(3)
            self.driver.execute_script(js)
            self.__writer_excel(True, "点击成功")
            return True
        except Exception as e:
            logger.exception(self.e)
            self.__writer_excel(False, traceback.format_exc())
            return False

    def input(self,locator,text):
        """
        输入文本
        @param locator:
        @param text:
        @return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False, self.e)
            return False

        try:
            text = self.__get_relations(text)
            ele.send_keys(text)
            self.__writer_excel(True, "输入成功")
            return True
        except Exception as e:
            logger.error(self.e)
            self.__writer_excel(False, traceback.format_exc())
            return False

    def inputfile(self,locator,text):
        """
        上传文件
        @param locator:
        @param text: 文件名字
        @return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False,self.e)
            return False
        try:
            text = sysKey.path + "\\lib\\file\\" + text #这里要是绝对路径
            ele.send_keys(text)
            self.__writer_excel(True,"上传文件成%s功"%text)
            return True
        except Exception as e:
            #logger.info(self.e)
            self.__writer_excel(False,traceback.format_exc())
            return False

    def sleep(self,t):
        """
        强制等待
        @param t:
        @return:
        """
        try:
            time.sleep(int(t))
            self.__writer_excel(True,"强制等待成功")
            return True
        except Exception as e:
            self.__writer_excel(False,traceback.format_exc())
            return False

    def quit(self):
        """
        退出浏览器
        :return:
        """
        try:
            self.driver.quit()
            self.__writer_excel(True, "退出浏览器成功")
            return True
        except Exception as e:
            self.__writer_excel(False, traceback.format_exc())
            return False

    def gettext(self, locator, param="text"):
        """
        获取元素文本 并且保存为关联后参数名 parama
        :param locator:
        :param param:
        :return:
        """
        ele = self.__findele(locator)
        if ele is None:
            self.__writer_excel(False, self.e)
            return False

        try:
            text = ele.text
            sysKey.relations[param] = text  # 设置关联字典
            self.__writer_excel(True, "获取文本%s成功" % text)
            return True
        except Exception as  e:
            self.__writer_excel(False, traceback.format_exc())
            return False

    def scrolltoend(self):
        """
        把页面直接滑动到底部
        :return:
        """
        js = "window.scrollTo(0, document.body.scrollHeight)"  # 滑动滚动条到底部
        try:
            self.driver.execute_script(js)
            self.__writer_excel(True, "页面滑动到底部成功")
            return True

        except Exception as e:
            logger.error(self.e)
            self.__writer_excel(False, "页面滑动到底部失败")
            return False

    def assertcontains(self, expect, actual):
        """
        断言关键字 是否包含预期
        :param expect: 预期
        :param actual: 实际
        :return:
        """
        actual = self.__get_relations(actual)
        expect = self.__get_relations(expect)

        if actual.__contains__(str(expect)):
            self.__writer_excel(True, actual)
            return True
        else:
            self.__writer_excel(False, actual)
            return False

    def __findele(self,locator):
        """
        通过定位找到元素
        @param locator: 元素 支持8种
        @return:
        """
        try:
            if locator.startswith("id="):
                locator = locator[locator.find('=')+1:]
                ele = self.driver.find_element_by_id(locator)
            elif locator.startswith("xpath="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_xpath(locator)
            elif locator.startswith("tagname="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_tag_name(locator)
            elif locator.startswith("name="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_name(locator)
            elif locator.startswith("linktext="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_link_text(locator)
            elif locator.startswith("css="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_css_selector(locator)
            elif locator.startswith("class="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_class_name(locator)
            elif locator.startswith("partial="):
                locator = locator[locator.find('=') + 1:]
                ele = self.driver.find_element_by_partial_link_text(locator)
            else:
                ele = self.driver.find_element_by_xpath(locator)
        except Exception as e:
            self.e = traceback.format_exc()
            return None

        return ele

    def slide(self,ele1xpath,ele2xpath):
        """
        破解滑块验证码
        @param ele1:滑块元素
        @param ele2:背景图片元素
        @return:
        """
        i = 0
        for i in range(10):
            time.sleep(5)

            ele1 = self.driver.find_element_by_xpath(ele1xpath)
            ele2 = self.driver.find_element_by_xpath(ele2xpath)
            get_img(ele1.get_attribute("src"), './lib/target.png')
            get_img(ele2.get_attribute("src"), './lib/template.png')

            x = FindPic()
            print(x)

            w1 = ele1.size['width']
            print(w1)
            img = cv2.imread('./lib/target.png')
            w2 = img.shape[1]
            print(w2)

            x = int(x * w1 / w2)
            # y = random.randint(1,10)
            print(x)
            # 滑动
            action = ActionChains(self.driver)
            action.click_and_hold(ele2)  # 按住元素
            action.move_by_offset(x, 0)
            # action.move_by_offset(x-y,0).perform() #滑动x和y
            # time.sleep(1)
            # action.move_by_offset(y,0)
            action.release().perform()  # 释放鼠标

            time.sleep(5)
            try:
                ele_res = self.driver.find_element_by_xpath('//*[contains(text(),"186****9614")]')
                self.__writer_excel(True,"破解滑块成功")
                break
            except Exception as  e:
                print("滑块验证失败")

            i += 1
            if i == 9:
                self.__writer_excel(False, "破解滑块失败")
    def __writer_excel(self, status, msg):
        """
        写入关键字运行结果
        :param status: 运行状态
        :param msg: 实际结果
        :return:
        """
        if status is True:
            self.writer.write(self.row, 7, "PASS", 3)
        else:
            self.writer.write(self.row, 7, "FAIL", 2)

        # 有时候实际结果过长，我们就只保存前1024个字符
        msg = str(msg)
        if len(msg) > 32767:
            msg = msg[0:32767]

        self.writer.write(self.row, 8, str(msg))

    def __get_relations(self,params):
        if params is None:
            return None
        else:
            params = str(params)

        for key in sysKey.relations.keys():
            params = params.replace("{" + key + "}",str(sysKey.relations[key]))
            return params

        return params