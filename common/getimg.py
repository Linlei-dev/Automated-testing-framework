# -*- coding: utf-8 -*-
# Powered By: ECHO
# @Time : 2020/8/22 15:26
"""
pip install -U opencv-python
"""
import cv2
import requests


def FindPic(target="./lib/target.png", template="./lib/template.png"):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    print(value)
    # 返回最佳匹配的x坐标
    return value[3][0]


def get_img(src, filepath):
    resp = requests.get(src)
    img = resp.content  # 二进制图片
    with open(filepath, "wb") as f:  # 二进制文件保存
        f.write(img)


if __name__ == "__main__":
    res = FindPic()
    print(res)
