
#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import os
import math
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt


def print_size(str, file_path):
    size = os.path.getsize(file_path)
    # print(str, size)
    return size


def do_restrore(result_name, restore_name):
    jump_restrore = False
    if (jump_restrore):
        return
    cv2.imwrite(restore_name, cv2.imread(result_name, 0)*16)
    print_size("restore: ", restore_name)


def get_two_names(prefix, fuc, divisor):
    result_name = "{0}_{1}_{2}.png".format(prefix, fuc, divisor)
    restore_name = "{0}_{1}_{2}_restore.bmp".format(prefix, fuc, divisor)
    return result_name, restore_name


# 对图像降低分辨率，cv2.pyrDown，太影响破损检测
def image_pyrDown(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "pyrDown", divisor)

    tmp = img
    for i in range(divisor-1):
        tmp = cv2.pyrDown(tmp)

    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    print_size("pyrDown result: ", result_name)
    do_restrore(result_name, restore_name)


record_raw = []
record_div = []
record_reduce = []
start_png_para = 1

# # 对图像作反色，几乎完全无效
# # 对图像作除法，效果明显


def image_div(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "div", divisor)
    cv2.imwrite(result_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record_div.append(print_size("div result: ", result_name))
    do_restrore(result_name, restore_name)


# 对图像降低分辨率，直接取左上角，效果明显
def image_reduce_resolution(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "reduce", divisor)

    row = int(120/divisor)
    col = int(160/divisor)
    tmp = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            tmp[i, j] = (img[i*divisor, j*divisor]).astype(np.uint8)

    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record_reduce.append(print_size("reduce result: ", result_name))
    do_restrore(result_name, restore_name)


def test_para_for_png(img, num, save_path, cnt):
    prefix = "{0}/{1}_{2}".format(save_path, num, cnt)
    png_name = "{0}.png".format(prefix)

    cv2.imwrite(png_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(png_name)
    record_raw.append(size)
    print("png: ", cnt, " ", size)

    # for divisor in range(2, 3):
    #     image_div(img, prefix, int(math.pow(2, divisor-1)))
    #     # image_pyrDown(img,  prefix, divisor)
    #     image_reduce_resolution(img,  prefix, divisor)
    image_div(img, prefix, 16)
    image_reduce_resolution(img,  prefix, 3)


def print_value(rects, offset):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/3. +
                 offset, 1.02*height, '%s' % (height))


def drawHistogram():
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号

    total_width, n = 0.5, 3   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    my_fontsize = 16
    x = np.arange(len(record_div))   # 横坐标范围

    plt.figure()
    plt.title("")
    plt.xlabel("png压缩级别", fontsize=my_fontsize)
    plt.xticks(x, range(start_png_para, 10))  # 设置x轴刻度显示值
    plt.ylabel("结果图片大小/Byte", fontsize=my_fontsize)
    rect0 = plt.bar(x - width, record_raw, width=width, label="raw")
    rect1 = plt.bar(x, record_div, width=width, label="div 16")
    rect2 = plt.bar(x + width, record_reduce, width=width, label="reduce 4")
    print_value(rect0, -0.13)
    print_value(rect1, -0.03)
    print_value(rect2, -0.05)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    # num_list = [421802, 418473, 461986, 518835, 504573,663392,845788]
    num_list = [421802]
    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        print_size("bmp: ", bmp_name)
        img = cv2.imread(bmp_name, 0)
        for cnt in range(start_png_para, 10):
            test_para_for_png(img, num, save_path, cnt)
    drawHistogram()
    print(record_div)
    print(record_reduce)
