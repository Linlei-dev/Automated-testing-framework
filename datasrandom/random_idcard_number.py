# -*- coding: utf-8 -*- 
# @Time : 2020-10-31 15:18 
# @Author : ECHO
# @File : random_idcard_number.py



import random
#随机生成符合业务场景的身份证后六位
class IDCARD:
    def idcard(self):
        headnumber = random.randint(0, 99999)
        if headnumber < 10:
            headnumber = "0000" + str(headnumber)
        elif headnumber < 100:
            headnumber = "000" + str(headnumber)
        elif headnumber < 1000:
            headnumber = "00" + str(headnumber)
        elif headnumber < 10000:
            headnumber = "0" + str(headnumber)
        else:
            headnumber = str(headnumber)

        last = ["0","1","2","3","4","5","6","7","8","9","x","X"]
        lastnumber = random.choice(last)

        idcardnumber = headnumber + lastnumber
        return idcardnumber

if __name__ == "__main__":
    idcard = IDCARD()
    print(idcard.idcard())


