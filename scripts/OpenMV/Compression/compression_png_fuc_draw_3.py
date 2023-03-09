
#!/usr/bin/python
# -*- coding: utf-8 -*-


import cv2
import os
from helpers import *


record_raw = []
record_div = []
record_reduce = []
start_png_para = 8


def test_para_for_png(img, num, save_path, cnt, record):
    prefix = "{0}/{1}_{2}".format(save_path, num, cnt)
    png_name = "{0}.png".format(prefix)

    cv2.imwrite(png_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(png_name)
    record.append(size)
    print("png: ", cnt, " ", size)

    image_div(img, prefix, cnt, 16, record_div)
    image_reduce_resolution(img,  prefix, cnt, 3, record_reduce)


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
            test_para_for_png(img, num, save_path, cnt, record_raw)
    drawHistogram_3(record_raw, record_div, record_reduce)
    print(record_raw)
    print(record_div)
    print(record_reduce)
