#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from helpers import *


record_div = []
record_reduce = []


def test_para_for_png(img, num, save_path, cnt):
    prefix = "{0}/{1}_{2}".format(save_path, num, cnt)
    png_name = "{0}.png".format(prefix)

    cv2.imwrite(png_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(png_name)
    print("png: ", cnt, " ", size)

    for divisor in range(1, 2):
        image_div(img, prefix, cnt, int(math.pow(2, divisor)), record_div)
        image_pyrDown(img,  prefix, cnt, divisor)
        image_reduce_resolution(img,  prefix, cnt, divisor, record_reduce)


def drawHistogram_2():
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号

    list1 = record_div
    list2 = record_reduce
    length = len(list1)
    x = np.arange(length)   # 横坐标范围

    plt.figure()
    total_width, n = 0.5, 2   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    x1 = x - width / 2   # 第一组数据柱状图横坐标起始位置
    x2 = x1 + width   # 第二组数据柱状图横坐标起始位置

    plt.title("")
    plt.xlabel("png压缩级别")
    plt.xticks(x, range(1, 10))  # 设置x轴刻度显示值
    plt.ylabel("结果图片大小/Byte")
    rect1 = plt.bar(x1, list1, width=width, label="div")
    rect2 = plt.bar(x2, list2, width=width, label="reduce")
    for rect in rect1:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2. -
                 0.12, 1.02*height, '%s' % (height))
    for rect in rect2:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2. -
                 0.1, 1.02*height, '%s' % (height))
    plt.legend()
    plt.show()


if __name__ == '__main__':

    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    num_list = [421802]
    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        print_size("bmp: ", bmp_name)

        img = cv2.imread(bmp_name, 0)
        for cnt in range(1, 10):
            test_para_for_png(img, num, save_path, cnt)

        drawHistogram_2()
        print(record_div)
        print(record_reduce)
        # record_div.clear()
        # record_reduce.clear()
