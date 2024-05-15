# -*- coding:utf-8 -*-
# @time:2020-9-10 14:35
# POWERD BY:ECHO


#
# def get_IDcard():
#     """
#     随机身份证后6位
#     """
import datasrandom

five = datasrandom.randint(0, 99999)
if five < 10:
    _five = "0000" + str(five)
elif five < 100:
    _five = "000" + str(five)
elif five < 1000:
    _five = "00" + str(five)
elif five < 10000:
    _five = "0" + str(five)
else:
    _five = str(five)
print(_five)

last = datasrandom.randint(0, 11)
if last == 10:
    last = "x"
if last == 11:
    last = "X"

idcard = str(_five) + str(last)
print(idcard)
# print(type(idcard))

top2 = int(idcard[0:2])
print(top2)
