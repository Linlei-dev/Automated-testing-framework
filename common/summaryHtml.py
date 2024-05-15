# -*- coding:utf-8 -*-
# @time:2020-9-6 22:37
# POWERD BY:ECHO
import time

from common.config import config
from common.excelResult import Res
from common.logger import logger
from common.txt import Txt


def summaryHtml(resultusecase, casename, nowtime, html):
    # 获取数据结果
    res = Res()
    summary = res.get_res(resultusecase % (casename, nowtime))
    groups = res.get_groups(resultusecase % (casename, nowtime))
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(summary)

    for key in summary.keys():

        if summary[key] == "PASS":
            html = html.replace(
                '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;">status</td>',
                '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;color:green;">Pass</td>')
        elif summary[key] == "FAIL":
            html = html.replace(
                '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;">status</td>',
                '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;color:red;">Fail</td>')
        else:
            html = html.replace(key, summary[key])

    # 获取分组显示
    tr = '<tr><td width="100" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">分组信息</td><td width="80" height="28" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">用例总数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">通过数</td><td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">状态</td></tr>'
    trs = ""
    logger.info("================================================")
    logger.info(groups)
    for i in range(len(groups)):
        tmp = tr.replace('分组信息', str(groups[i][0]))
        tmp = tmp.replace('用例总数', str(groups[i][1]))
        tmp = tmp.replace('通过数', str(groups[i][2]))
        tmp = tmp.replace('状态', str(groups[i][3]))
        trs += tmp

    html = html.replace("mailbody", trs)
    html = html.replace('<td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">fail</td>',
                        '<td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;color: red;">fail</td>')
    html = html.replace('<td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;">pass</td>',
                        '<td width="80" align="center" bgcolor="#FFFFFF" style="border:1px solid #ccc;color: green;">pass</td>')
    html = html.replace('<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;">Fail</td>',
                        '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;color: red;">Fail</td>')
    html = html.replace('<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;">Pass</td>',
                        '<td height="28" bgcolor="#FFFFFF" align="center" style="border:1px solid #ccc;color: red;">Pass</td>')
    print(html)
    return html
