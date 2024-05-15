# -*- conding:utf-8 -*-
# @time:2020-8-8 15:14
# POWERD BY:Echo
import os
import threading
import time
import traceback
from common.commonKeys import sysKey
from common.logger import logger
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from common.newExcel import Reader, Writer


class APP:
    """
    APP自动化框架关键字
    """
    def __init__(self,writer):
        self.writer = writer
        self.row = 0
        self.conf = {} #保存appium配置
        self.driver = None
        self.e = None

    def startappium(self,port=""):
        """
        启动命令行版本的appium
        """
        logger.info("启动appium命令行版本")
        if port == "":
            port = "4723"
        self.conf["port"] = port

        def runappium(port = "4723"):
            cmd = r"appium -a 127.0.0.1 -p " + port
            os.popen(cmd).read()
            #logger.info(res)

        th = threading.Thread(target=runappium,args=())
        th.start()
        time.sleep(5)
        self.__write_excel(True,"打开appium成功")
        logger.info("创建子线程")

    def stopappium(self,port=""):
        logger.info("关闭appium进程")
        if port == "":
            port = "4723"
        try:
            pid = os.popen("netstat -aon | findstr LISTENING | findstr " + port).read()
            pid = pid.split(" ")
            if len(pid) < 2:
                return
            else:
                pid = pid[len(pid)-1]

            res = os.popen("taskkill /F /PID " + pid).read()
            logger.info(res)
            self.__write_excel(True,"关闭appium成功")

        except Exception as  e:
            self.__write_excel(False,traceback.format_exc())

    def startapp(self,conf):
        """
        启动app
        :param conf:{
                      "platformName": "Android",
                      "platformVersion": "5.1.1",
                      "deviceName": "127.0.0.1:62001",
                      "appPackage": "com.tencent.mm",
                      "appActivity": ".ui.LauncherUI",
                      "noReset": True,
                      "unicodeKeyboard": True,
                      "resetKeyboard": True,
                      "automationName": "UiAutomator1"
                    }
        :return:
         "automationName": "UiAutomator1"  这个用来测试小程序
        """
        try:
            conf = conf.replace(r"\n","")
            conf = eval(conf)
            logger.info("启动APP，其配置为：" + str(conf))
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            self.writer.save_close()
            self.startappium(self.conf["port"])
            exit(-1)
            return False
        try:
            self.conf.update(conf)
            self.driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub",conf)
            self.driver.implicitly_wait(20)
            self.__write_excel(True,"start APP success")
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            self.writer.save_close()
            logger.info("start APP fail")
            self.stopappium(self.conf["port"])
            exit(-1)
            return False

    def sleep(self,t):
        """
        强制等待
        """
        logger.info("强制等待%s秒"%t)
        try:
            time.sleep(int(t))
            self.__write_excel(True,"wait")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def wait_ele(self,locator):
        """
        判定元素是否出现
        """
        logger.info("判定元素%s是否出现"%locator)
        ele = self.__findele(locator)
        if ele == None:
            self.__write_excel(False,"等待失败")
        else:
            self.__write_excel(True,"等待成功")

    def slide(self,p1,p2):
        """
        滑动坐标
        p1:1,1
        p1:2,2
        """
        try:
            p1 = p1.split(",")
            p2 = p2.split(",")
            TouchAction(self.driver).press(x=int(p1[0]),y=int(p1[1])).move_to(x=int(p2[0]),y=int(p2[1])).release().perform()
            self.__write_excel(True,"滑动成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def input(self,locator,text,t=""):
        """
        输入文字
        """
        if t == "":
            t = 5
        time.sleep(int(t))

        ele = self.__findele(locator)
        if ele is None:
            self.__write_excel(False,"定位元素失败")
            return False
        try:
            text = self.__get_relations(text)
            ele.send_keys(text)
            self.__write_excel(True,"输入元素成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def gettext(self,locator,param="text",t=""):
        """
        获取元素文本 并且保存为关联后参数名字为param
        """
        if t == "":
            t = 10
        time.sleep(int(t))

        ele = self.__findele(locator)
        if ele is None:
            self.__write_excel(False,self.e)
            return False
        try:
            text = ele.text
            sysKey.relations[param] = text
            self.__write_excel(True,"获取元素文本成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def assertcontains(self,expect,actual):
        """
        断言关键字 实际结果是否包含期望结果
        """
        #关联
        actual = self.__get_relations(actual)
        expect = self.__get_relations(expect)

        if actual.__contains__(str(expect)):
            self.__write_excel(True,actual)
        else:
            self.__write_excel(False,actual)
            return False

    def assertequal(self,expect,actual):
        actual = self.__get_relations(actual)
        expect = self.__get_relations(expect)

        if actual == expect:
            self.__write_excel(True,actual)
        else:
            self.__write_excel(False,actual)



    def click(self,loctor,t=""):
        if t == "":
            t = 5
        time.sleep(int(t))

        ele = self.__findele(loctor)
        if ele is None:
            self.__write_excel(False,self.e)
            return False
        try:
            ele.click()
            self.__write_excel(True,"点击成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def adbclick(self,x,y,t=""):
        if t == "":
            t = 5
        time.sleep(int(t))

        try:
            logger.info("adb shell input tap %s %s"%(x,y))
            os.popen("adb shell input tap %s %s"%(x,y)).read()
            self.__write_excel(True,"adb点击成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False

    def quit(self):
        try:
            self.driver.quit()
            self.__write_excel(True,"退出app成功")
            return True
        except Exception as e:
            self.__write_excel(False,traceback.format_exc())
            return False


    def __write_excel(self,status,msg):
        if status == True:
            self.writer.write(self.row,7,"PASS",3)
        else:
            self.writer.write(self.row,7,"FAIL",2)

        msg = str(msg)
        if len(msg) > 32767:
            msg = msg[0:32767]
        self.writer.write(self.row,8,msg)


    def __findele(self,locator):
        try:
            if locator.startswith("/"):
                ele = self.driver.find_element_by_xpath(locator)
            elif locator.index(":id/") > 0:
                ele = self.driver.find_element_by_id(locator)
            else:
                ele = self.driver.find_element_by_accessibility_id(locator)

        except Exception as e:
            self.e = traceback.format_exc()
            return  None

        return ele

    def __get_relations(self,params):
        if params is None:
            return None
        else:
            params = str(params)

        for key in sysKey.relations.keys():
            params = params.replace("{" + key + "}",str(sysKey.relations[key]))
            return params

        return params




if __name__ == "__main__":
    conf = {
                      "platformName": "Android",
                      "platformVersion": "6.0.1",
                      "deviceName": "6HJ4C20110006671",
                      "appPackage": "com.evergrande.bao.consumer",
                      "appActivity": ".splash.SplashActivity",
                      "noReset": True,
                      "unicodeKeyboard": True,
                      "resetKeyboard": True,
                      "automationName": "UiAutomator1"
                    }
    reader = Reader()
    # reader.open_excel("../lib/apptest.xlsx")
    writer = Writer()
    # writer.copy_open("../lib/apptest.xlsx","../lib/apptestres.xlsx")
    app = APP(writer)
    app.startappium()







