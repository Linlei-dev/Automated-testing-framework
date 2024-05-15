# -*- coding:utf-8 -*-
# @time:2020-9-6 21:23
# POWERD BY:ECHO
import inspect


def getfunc(obj, method):
    """
    反射获取函数和参数列表
    :param obj: 对象
    :param method: 方法名
    :return:
    """
    try:
        func = getattr(obj, method)
    except Exception as e:
        return None

    arg = inspect.getfullargspec(func).__str__()
    arg = arg[arg.find('args=') + 5:arg.find(', varargs')]
    arg = eval(arg)
    arg.remove('self')
    return func, len(arg)

