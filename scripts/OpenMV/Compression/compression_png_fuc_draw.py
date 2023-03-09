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

    my_fontsize = 16
    list1 = record_div
    list2 = record_reduce
    x = np.arange(len(list1))   # 横坐标范围

    plt.figure()
    total_width, n = 0.5, 2   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    plt.title("")
    plt.xlabel("png压缩级别", fontsize=my_fontsize)
    plt.xticks(x, range(1, 10))  # 设置x轴刻度显示值
    plt.ylabel("结果图片大小/Byte", fontsize=my_fontsize)
    rect1 = plt.bar(x - width / 2, list1, width=width, label="div")
    rect2 = plt.bar(x + width / 2, list2, width=width, label="reduce")
    print_value(rect1, -0.2)
    print_value(rect2, -0.2)

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
