# -*- coding:utf-8 -*-
# @time:2020-9-7 11:25
# POWERD BY:ECHO
import hashlib
import hmac
import json
import time
import traceback
import jsonpath
import requests
import datetime

from common.commonKeys import sysKey
from common.logger import logger
from common.mysql import Mysql
from datasrandom.random_idcard_number import IDCARD
from datasrandom.random_phone_number import phoneNumber


class HTTP:
    def __init__(self, writer):
        self.session = requests.session()
        # 设置请求默认的头
        self.session.headers["content-type"] = 'application/json; charset=utf-8'
        self.session.headers[
            'user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
        self.session.headers["terminalType"] = "android"
        self.url = ""
        self.result = None
        self.jsonres = None
        self.writer = writer
        self.row = 0
        self.e = None
        self.count_overtime = 0  # 统计超时的接口数目
        self.day = ""
        self.time = ""

    def seturl(self, url):
        """
        设置接口项目基本地址
        @param url: 项目基本地址
        @return:
        """
        if url is None or url == "":
            url = ""
        self.url = url
        self.__write_excel(True, self.url)
        return True

    def get(self, path, params):
        if params is None or params == "":
            params = None
        if path is None or path == "":
            self.__write_excel(False, "接口错误，接口地址不能为空")

        params = self.__get_relations(params)

        if not path.startswith("http"):
            path = self.url + "/" + path
        if params:
            try:
                start_time = time.time()
                self.result = self.session.get(path + "?" + params)
                end_time = time.time()
                cost_time = end_time - start_time
                if cost_time > 500:
                    self.writer.write(self.row, 9, str(cost_time), 2)
                    self.count_overtime = self.count_overtime + 1
                else:
                    self.writer.write(self.row, 9, str(cost_time), 3)
                # 如果有接口请求耗时大于500ms，用红色写入，否则用绿色
                if self.count_overtime > 0:
                    self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 2)
                else:
                    self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 3)
            except Exception as e:
                self.result = None
        else:
            try:
                start_time = time.time()
                self.result = self.session.get(path)
                end_time = time.time()
                cost_time = end_time - start_time
                if cost_time > 500:
                    self.writer.write(self.row, 9, str(cost_time), 2)
                    self.count_overtime = self.count_overtime + 1
                else:
                    self.writer.write(self.row, 9, str(cost_time), 3)
                if self.count_overtime > 0:
                    self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 2)
                else:
                    self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 3)
            except Exception as e:
                self.result = None

        try:
            # 如果返回json字符串就处理为字典
            resulttext = self.result.text
            resulttext = resulttext[resulttext.find("{"):resulttext.rfind("}") + 1]
            self.jsonres = json.loads(resulttext)
            self.__write_excel(True, self.jsonres)
        except Exception as e:
            logger.exception(e)
            self.jsonres = None
            self.__write_excel(False, None)

        return True

    def fcb_get(self, path, params=""):
        """
        房车宝一些get接口是返回网页并且断言
        :param path:
        :param params:
        :return:
        """
        if params is None or params == "":
            params = None
        if path is None or path == "":
            self.__write_excel(False, "接口错误，接口地址不能为空")

        params = self.__get_relations(params)

        if not path.startswith("http"):
            path = self.url + "/" + path

        try:
            if params is not None:
                self.result = self.session.get(path + "?" + params)
            else:
                self.result = self.session.get(path)

            self.__write_excel(True, self.result.text)
        except Exception as e:
            self.__write_excel(False, e)
            return False
        return True

    def post(self, path, params):
        """
        data用字典传参数 可以传入键值对字符 会帮转字典
        @param path:
        @param params:
        @return:
        """
        if params is None or params == "":
            params = None
        if path is None or path == "":
            self.__write_excel(False, "接口路径不能为空")
            return False

        params = self.__get_relations(params)  # 把关联动态参数替换为储存的值
        # params = self.__get_data(params)
        params = self.__str_to_dic(params)

        if not path.startswith("http"):
            path = self.url + path

        try:
            start_time = time.time()
            self.result = self.session.post(path, json=params)
            end_time = time.time()
            cost_time = int((end_time - start_time) * 1000)
            if cost_time > 500:
                self.writer.write(self.row, 9, str(cost_time), 2)
                self.count_overtime = self.count_overtime + 1
            else:
                self.writer.write(self.row, 9, str(cost_time), 3)
            # 如果有接口请求耗时大于500ms，用红色写入，否则用绿色
            if self.count_overtime > 0:
                self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 2)
            else:
                self.writer.write(1, 9, "注意：本次自动化接口测试截至当前页共有%d条接口响应耗时超过500ms!" % self.count_overtime, 3)
        except Exception as e:
            self.result = None
            self.writer.write(self.row, 9, "该接口请求出错！！！", 2)
            return False

        try:
            # 如果返回json 处理为字典
            resulttext = self.result.text
            # print(resulttext)
            resulttext = resulttext[resulttext.find("{"):resulttext.rfind("}") + 1]

            self.jsonres = json.loads(resulttext)  # 字典转json格式
            self.__write_excel(True, self.jsonres)

        except Exception as e:
            logger.exception(e)
            print(self.jsonres)
            print(path)
            self.jsonres = None
            self.__write_excel(False, e)
            return False

        return True

    def post_test(self, path, params):
        if path is None or path == "":
            self.__write_excel(False, "接口路径不能为空")
            return False
        # str转字典
        params = self.__str_to_dic(params)
        # print(params)
        # print(type(params))
        # 拼接域名地址和路径
        if not path.startswith("http"):
            path = self.url + path
        # print(path)
        try:
            start_time = time.time()
            self.result = self.session.post(path, json=params)
            end_time = time.time()
            cost_time = (end_time - start_time) * 1000
            resulttext = self.result.text
            self.jsonres = json.loads(resulttext)
            # print(self.jsonres)
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            self.__write_excel(True, self.jsonres)
            if cost_time > 500:
                self.writer.write(self.row, 9, str(cost_time), 3)
            else:
                self.writer.write(self.row, 9, str(cost_time), 2)
            return True
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            self.writer.write(self.row, 9, "该接口请求出错！！！", 2)
            return False

    def postNodata(self, path, params):
        """
        以字典形式传键值对参数
        @param path:
        @param params:
        @return:
        """
        if params is None or params == "":
            params = None
        if path is None or path == "":
            self.__write_excel(False, "接口地址不能为空")
            return False

        params = self.__get_relations(params)

        if not path.startswith("http"):
            path = self.url + path

        try:
            self.result = self.session.post(path, data=params)
        except Exception as e:
            self.result = None

        try:
            resulttext = self.result.text
            resulttext = resulttext[resulttext.find("{"):resulttext.rfind("}") + 1]
            self.jsonres = json.loads(resulttext)
            self.__write_excel(True, self.jsonres)
        except Exception as e:
            logger.exception(e)
            self.jsonres = None
            self.__write_excel(False, None)

        return True

    # 当post请求的参数在url中时，使用此方法
    def postNoparams(self, path, params):
        """
        将参数拼接在url中请求
        @param path:
        @param params:
        @return:
        """
        if params is None or params == "":
            params = None
        if path is None or path == "":
            self.__write_excel(False, "接口地址不能为空")
            return False

        params = self.__get_relations(params)

        if not path.startswith("http"):
            path = self.url + path + params

        try:
            self.result = self.session.post(url=path)
        except Exception as e:
            self.result = None

        try:
            resulttext = self.result.text
            resulttext = resulttext[resulttext.find("{"):resulttext.rfind("}") + 1]
            self.jsonres = json.loads(resulttext)
            self.__write_excel(True, self.jsonres)
        except Exception as e:
            logger.exception(e)
            self.jsonres = None
            self.__write_excel(False, None)

        return True

    def addheader(self, key, vaule):
        """
        添加请求头
        @param key:
        @param vaule:
        @return:
        """
        vaule = self.__get_relations(vaule)
        try:
            self.session.headers[key] = vaule
            self.__write_excel(True, vaule)
            return True
        except Exception as e:
            logger.exception(e)
            self.__write_excel(False, "添加请求头失败")
            return False

    def removeheader(self, key):
        """
        删除头
        @param key:
        @return:
        """
        try:
            self.session.headers.pop(key)
            self.__write_excel(True, "删除请求头" + key + "成功")
            return True
        except Exception as e:
            logger.error(e)
            self.__write_excel(False, traceback.format_exc())
            return False

    def savejson(self, json_path, paramname):
        """
        从返回的json里面取值 保存json里面的键的值到公共字典
        @param jsonpath:
        @param paramname:
        @return:
        """
        try:
            value = str((jsonpath.jsonpath(self.jsonres, json_path))[0])
            sysKey.relations[paramname] = value
            self.__write_excel(True, "保存" + str(paramname) + "=" + str(value) + "到公共字典成功")
            return True
        except Exception as e:
            logger.exception(e)
            self.__write_excel(False, traceback.format_exc())
            return False

    def savejson_int(self, json_path, paramname):
        """
        从返回的json里面取值 保存json里面的键的值到公共字典
        @param jsonpath:
        @param paramname:
        @return:
        """
        try:
            value = str((jsonpath.jsonpath(self.jsonres, json_path)))
            sysKey.relations[paramname] = value
            self.__write_excel(True, "保存" + str(paramname) + "=" + str(value) + "到公共字典成功")
            return True
        except Exception as e:
            logger.exception(e)
            self.__write_excel(False, traceback.format_exc())
            return False

    def save_variable(self, key, value):
        """
        保存变量到公共字典
        :param key:
        :param value:
        :return:
        """
        try:
            sysKey.relations[key] = value
            self.__write_excel(True, "保存变量" + str(key) + "=" + str(value) + "到公共字典成功！")
            return True
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            return False

    def add_timestamp(self):
        """
        产生时间戳并且存到请求头 注意我们是毫秒的时间戳
        :return:
        """
        timestamp = int(time.time() * 1000)
        self.session.headers["timestamp"] = str(timestamp)
        self.__write_excel(True, "生成时间戳：" + str(timestamp) + "并且存到请求头")
        return True

    def save_now_date(self, key):
        """
        获取系统当前日期
        """
        self.day = datetime.date.today()
        self.save_variable(key, self.day)
        return True

    def save_now_time(self, key):
        """
        获取系统当前日期和时间并格式化
        """
        self.time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_variable(key, self.time)
        return True

    def add_sign(self, key="hdboms"):
        """
        HMAC+SHA256加密获取签名；并且把签名添加到请求头
        :param key:  如果是b c端app 就是默认值；如果是案场宝app就是hdbscene
        :return:
        """
        strTime = "timestamp="
        strToken = "&token="
        strUnionId = "&unionId="
        s = strTime + self.session.headers["timestamp"] + strToken + self.session.headers["Authorization"] + \
            strUnionId + self.session.headers["unionId"]
        s = "111111"
        print(s)
        try:
            sign = hmac.new(key.encode(), s.encode(), digestmod=hashlib.sha256).hexdigest().upper()
            print(sign)
        except Exception as e:
            self.__write_excel(False, str(e) + "加密获取sign失败")
            return False
        else:
            # 把签名添加到请求头
            self.session.headers["sign"] = sign
            self.__write_excel(True, "请求头中添加sign：" + ">>>" + self.session.headers["sign"] + ">>>" +
                               self.session.headers["timestamp"] + ">>>" + self.session.headers[
                                   "Authorization"] + ">>>" + self.session.headers["unionId"])
            print(self.session.headers)
        return True

    def assertequaljson(self, jsonexp):
        """
        断言json结果里面的多个键值对是否相等
        @param jsonexp: 传入完整的预期的键值对json字符串
        @return:
        """
        if self.jsonres is None:
            self.__write_excel(False, None)
            return False
        try:
            jsonexp = json.loads(jsonexp)  # 如果传入的参数不是json 会报错
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            return False
        try:
            for key in jsonexp.keys():
                value = str(jsonpath.jsonpath(self.jsonres, key)[0])
                if not value == str(jsonexp[key]):  # 如果有一个键值对和预期不符合 就失败
                    self.__write_excel(False, self.jsonres)
                    return False
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            return False

        self.__write_excel(True, self.jsonres)
        return True

    def assertcontains(self, value):
        """
        断言返回结果的字符串包含value
        :param value: 被包含的字符串
        :return: 是否包含
        """
        try:
            # 如果返回结果为空，就报错
            result = str(self.result.text)
        except Exception as e:
            self.__write_excel(False, e)
            return False

        value = self.__get_relations(value)

        if result.__contains__(str(value)):
            self.__write_excel(True, self.result.text)
            return True
        else:
            self.__write_excel(False, self.result.text)
            return False

    def excute_sql(self, sql):
        """
        执行sql语句,相关数据库配置在配置文件
        :param sql:
        :return:
        """
        if sql == "" or sql is None:
            sql = None
            self.__write_excel(False, "sql语句不能为空")
            return False
        mysql = Mysql()
        # 执行sql语句 返回一个元组
        try:
            res = mysql.select_mysql(sql)
            self.__write_excel(True, res)
            return True
        except Exception as e:
            self.__write_excel(False, traceback.format_exc())
            return False

    def __write_excel(self, status, msg):
        if status is True:
            self.writer.write(self.row, 7, "PASS", 3)
        else:
            self.writer.write(self.row, 7, "FAIL", 2)

        msg = str(msg)
        if len(msg) > 32767:
            msg = msg[0:32767]
        self.writer.write(self.row, 8, str(msg))

    def __get_relations(self, params):
        """
        如果是传递的变量{key}，去公共字典取值
        :param params:
        :return:
        """
        if params is None:
            return None

        for key in sysKey.relations.keys():
            params = params.replace("${" + key + "}", str(sysKey.relations[key]))
        return params

    def __get_data(self, params):
        """
        url 参数转字典
        @param params:
        @return:
        """
        if params is None:
            return None
        param = {}
        p1 = params.split("&")
        for keyvalue in p1:
            index = keyvalue.find("&")
            if index >= 0:
                key = keyvalue[0:index]
                value = keyvalue[index + 1:]
                param[key] = value
            else:
                param[keyvalue] = ""
        return param

    def __str_to_dic(self, params):
        """
        填入的json字符串 转字典
        :param params:
        :return:
        """
        if params is None:
            return None
        try:
            param = json.loads(params)
        except Exception as e:
            logger.error(e)
            return None
        return param

    def spliceAuthorization(self, a: str, b: str, name):
        """
        把云鲸登录的信息的的token相关信息拼接下，并且保存到公共字典
        :param a: 第一个信息
        :param b: 第二个信息
        :param name: 保存的key
        :return:
        """
        a = self.__get_relations(a)
        b = self.__get_relations(b)
        try:
            s = a + " " + b
            self.__write_excel(True, s)
            sysKey.relations[name] = s

        except Exception as e:
            self.__write_excel(True, traceback.format_exc())
            return False
        return True
