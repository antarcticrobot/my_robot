#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import os
import math
from helpers import *


record_raw = []
record_div = []
record_shrink = []
start_png_para = 1


def test_para_for_png(img, num, save_path, cnt, record):
    prefix = "{0}/{1}_{2}".format(save_path, num, cnt)
    png_name = "{0}.png".format(prefix)

    cv2.imwrite(png_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(png_name)
    record.append(size)
    print("png: ", cnt, " ", size)

    for divisor in range(3, 4):
        image_div(img, prefix, cnt, int(math.pow(2, divisor-1)), list_div)
        image_pyrDown(img,  prefix, cnt, divisor)
        image_shrink(img,  prefix, cnt, divisor, list_shrink)


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    # num_list = [421802, 418473, 461986, 518835, 504573, 663392, 845788]
    num_list = [421802]
    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        print_size("bmp: ", bmp_name)
        img = cv2.imread(bmp_name, 0)

        tmp = []
        list_div = []
        list_shrink = []
        for cnt in range(start_png_para, 10):
            test_para_for_png(img, num, save_path, cnt, tmp)
        record_raw.append(tmp)
        record_div.append(list_div)
        record_shrink.append(list_shrink)

    drawHistogram_3(record_raw, record_div, record_shrink,
                    "raw", "div", "shrink", -0.25, -0.1, -0.15)

    print(record_raw)
    print(record_div)
    print(record_shrink)
