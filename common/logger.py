# -*- conding:utf-8 -*-
# @time:2020-8-8 15:27
# POWERD BY:Echo
import logging

path = ""
logger = None
# create logger
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
c = logging.FileHandler(path + "logs/all.log", mode='a', encoding='utf8')
logger = logging.getLogger('frame log')
logger.setLevel(logging.DEBUG)
c.setFormatter(formatter)
logger.addHandler(c)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# 打印日志级别
def debug(ss):
    global logger
    try:
        logger.debug(ss)
    except:
        return


def info(str):
    global logger
    try:
        logger.info(str)
    except:
        return


def warn(ss):
    global logger
    try:
        logger.warning(ss)
    except:
        return


def error(e):
    global logger
    try:
        logger.error(e)
    except:
        return


def exception(e):
    global logger
    try:
        logger.exception(e)
    except:
        return


if __name__ == "__main__":
    debug("1111")
    info("2222")
    warn("3333")
    error("44444")
    exception("555555")
