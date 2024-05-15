# -*- coding:utf-8 -*-
# @time:2020-9-6 21:45
# POWERD BY:ECHO
from common.logger import logger
from common.getfunc import getfunc


def runcase(obj, line):
    # print(line)

    if len(line[0]) > 0 or len((line[1])) > 0:
        # 分组信息不执行
        return

    func = getfunc(obj, line[3])
    if func is None:
        logger.warn(line[2] + "关键字%s不存在" % line[3])
        return

    if func[1] == 0:
        func[0]()
    elif func[1] == 1:
        func[0](line[4])
    elif func[1] == 2:
        func[0](line[4], line[5])
    elif func[1] == 3:
        func[0](line[4], line[5], line[6])
    else:
        logger.warn("关键字暂不支持超过3个参数")
