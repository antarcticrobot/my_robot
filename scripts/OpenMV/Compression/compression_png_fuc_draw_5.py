
#!/usr/bin/python
# -*- coding: utf-8 -*-
# 改自3
# 临界条件即"div 16"+"shrink 3"，纵轴从1-9的png压缩级别改成不同角度的图像


import cv2
import os
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

    image_shrink(img,  prefix, cnt, 3, list_shrink)
    image_div(img, prefix, cnt, 16, list_div)


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    num_lists = [[380295, 380771, 381246, 381724, 382194, 382672, 383147, 383623, 384098, 384573], [415620, 416095, 416566, 417046, 417521, 417997, 418473, 418949, 419436, 419902], [458414, 459008, 459679, 460203, 460828, 461422, 461986, 462614, 463202, 463789], [471518, 472114, 472710, 473301, 473894, 474487, 475083, 475674, 476270, 476866], [499342, 499933, 500531, 501125, 510989, 511703, 512415, 513131, 523827, 524573], [
        542372, 543085, 543798, 544511, 555798, 556511, 557225, 557938, 568075, 568757], [576734, 577447, 578159, 578873, 579583, 580299, 581013, 581726, 582445, 583273], [614173, 615006, 615837, 616665, 617500, 618332, 619163, 619995, 620827, 621665], [656737, 657566, 658398, 659229, 660060, 660897, 661731, 662564, 663392, 664222], [772249, 773201, 774155, 775101, 776047, 777002, 777954, 778905, 779859, 780808]]

    for num_list in num_lists:
        tmp = []
        list_div = []
        list_shrink = []

        for num in num_list:
            bmp_name = read_path+str(num)+".bmp"
            print_size("bmp: ", bmp_name)
            img = cv2.imread(bmp_name, 0)
            test_para_for_png(img, num, save_path, 9, tmp)

        record_raw.append(tmp)
        record_div.append(list_div)
        record_shrink.append(list_shrink)

    lists = [record_raw, record_div, record_shrink]
    drawHistogram_3(lists,  # ["raw", "div 16", "shrink 3"], [-0.25, -0.1, -0.15])
                    ["raw", "div 16", "shrink 3"], [-0.35, -0.15, -0.15])
    print(record_raw)
    print(record_div)
    print(record_shrink)