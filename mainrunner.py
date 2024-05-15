# -*- coding:utf-8 -*-
# @time:2020-9-6 21:09
# POWERD BY:ECHO

# -*- conding:utf-8 -*-
# @time:2020-8-9 17:11
# POWERD BY:Echo
import os
import time

# from APP.appKeys import APP
from HTTP.httpKeys import HTTP
from WEB.webKeys import WEB
from common import config, runcase, summaryHtml
from common.logger import logger
from common.mail import Mail
from common.newExcel import Reader, Writer
from common.txt import Txt

logger.info("开始运行测试用例")

casename = "best_after_sale_case"  # 执行用例的用例名，暂时只支持xlsx格式的用例
conf = "./lib/conf/conf.properties"  # 配置文件
usecase = './lib/cases/%s.xlsx'  # 执行的用例
resultusecase = './lib/cases/%s%s.xlsx'  # 执行完后生成的结果用例

# 初始化配置
config.get_config(conf)

nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())  # 结果用例生成时间，给结果用例命名
# print(nowtime)

reader = Reader()
reader.open_excel(usecase % casename)
writer = Writer()
writer.copy_open(usecase % casename, resultusecase % (casename, nowtime))

sheetname = reader.get_sheets()
starttime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

writer.set_sheet(sheetname[0])
writer.write(1, 3, starttime)  # 给用例里面写入开始时间，后面会写结束时间，方便邮件统计

# 实例对象 默认是app
# app = APP(writer)
web = WEB(writer)
http = HTTP(writer)
# obj = app
# logger.info(obj.driver)

for sheet in sheetname:
    # 设置当前读取的sheet页面
    reader.set_sheet(sheet)
    writer.set_sheet(sheet)
    lines = reader.readline()
    # 分类执行用例 在用例第一个页面 第二行 第二个单元格来判定执行条用什么方法
    line = lines[1]
    if str(line[1]).upper() == "HTTP":
        obj = http
    elif str(line[1]).upper() == "WEB":
        obj = web
    # elif str(line[1]).upper() == "APP":
    #    obj = app
    else:
        obj = http

# logger.info(obj.driver)

for sheet in sheetname:
    reader.set_sheet(sheet)
    writer.set_sheet(sheet)

    lines = reader.readline()

    for i in range(reader.rows):
        obj.row = i
        print(sheet + str(obj.row))
        line = lines[i]
        runcase.runcase(obj, line)  # 运行数据驱动

endtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

writer.set_sheet(writer.get_sheets()[0])
writer.write(1, 4, endtime)

writer.save_close()

# # 读取网页模版文件
# txt = Txt("./lib/conf/" + config.config["mailtxt"])
# html = txt.read()[0]
#
# # #替换汇总信息
# html = summaryHtml.summaryHtml(resultusecase, casename, nowtime, html)
# # 发送邮件
# mail = Mail()
# mail.mail_info["filepaths"] = ["./lib/cases/%s%s.xlsx" % (casename, nowtime)]
# path = os.getcwd()
# filepaths = path + r"\lib\cases\%s%s.xlsx" % (casename, nowtime)
# filename = "%s%s.xlsx" % (casename, nowtime)
# mail.mail_info["filepaths"] = [filepaths]
# mail.mail_info["filenames"] = ["%s%s.xlsx" % (casename, nowtime)]
#
# mail.send(html)

logger.info("测试用例运行结束")
