# -*- coding: utf-8 -*- 
# @Time : 2020-10-31 15:18 
# @Author : ECHO
# @File : random_phone_number.py
import random

class phoneNumber:
    def phoneNumber(self):
        headList = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139",
                       "145", "146", "147",
                       "150", "151", "152", "153", "155", "156", "158", "159",
                       "172", "174", "175", "176", "178",
                       "180", "181", "182", "183", "185", "186", "187", "188",
                       "198", "199"
                       ]
        headnumber = random.choice(headList)
        lastnumber = random.randint(0, 99999999)
        if lastnumber < 10000000:
            lastnumber = "0" + str(lastnumber)
        elif lastnumber < 1000000:
            lastnumber = "00" + str(lastnumber)
        elif lastnumber < 100000:
            lastnumber = "000" + str(lastnumber)
        elif lastnumber < 10000:
            lastnumber = "0000" + str(lastnumber)
        elif lastnumber < 1000:
            lastnumber = "00000" + str(lastnumber)
        elif lastnumber < 100:
            lastnumber = "000000" + str(lastnumber)
        elif lastnumber < 100:
            lastnumber = "0000000" + str(lastnumber)
        else:
            lastnumber = str(lastnumber)
        phone_number = headnumber + lastnumber

        return phone_number

if __name__ == "__main__":
    phone = phoneNumber()
    print(phone.phoneNumber())