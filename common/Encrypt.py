# -*- coding: utf-8 -*-
# Powered By: ECHO
# @Time : 2020/12/13 20:58

# pip install jpype1 == 0.7.0
# 导出加密解密的jar包
# python运行java库的原理：调用jvm虚拟机运行class文件
import os

import jpype

instance = None


def init():
    global instance
    # 需要导入jar包的位置
    jarpath = "../lib/conf/Encrypt.jar"
    # 获取java安装路径
    jdkpath = os.environ["JAVA_HOME"]

    # 启动jvm 加载jar 当有依赖包的时候一定要使用 -Djava.ext.dirs参数进行引入
    jpype.startJVM(jdkpath + "/jre/bin/server/jvm.dll", "-Djava.class.path=%s" % jarpath, convertStrings=False)
    # 获取jar中的类
    JClass = jpype.JClass("com.kc.Encrypt.Encrypt")
    # 初始化类 就是执行构造函数
    instance = JClass()


def encrypt(s):
    """
    加密函数
    :param s:需要加密的字符串
    :return:
    """
    global instance
    res = str(instance.enCrypt(s))
    return res


def decrypt(s):
    """
    解密函数
    :param s:需要解密的字符串
    :return:
    """
    global instance
    res = str(instance.deCrypt(s))
    return res


def shutdown():
    """
    关闭jvm
    :return:
    """
    jpype.shutdownJVM()


if __name__ == "__main__":
    init()
    res = encrypt("1234561111")
    print(res)
    res = decrypt(res)
    print(res)
