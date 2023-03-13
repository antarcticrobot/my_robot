
#!/usr/bin/python
# -*- coding: utf-8 -*-

# 临界条件即"div 16"+"shrink 3"，在1-10的拍摄组别下


import cv2
from helpers import *


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'
    num_list = [421802, 418473, 461986, 518835, 504573,
                663392, 845788, 383147, 388378, 393608, 396942,
                663392, 845788, 383147, 388378, 393608, 396942]  # 这行是重复的

    record = [[], [], []]
    for num in num_list:
        img = cv2.imread(read_path+str(num)+".bmp", 0)
        tmp = [[], [], []]
        test_para_for_png(img, num, save_path, 9, tmp, my_process_2)
        for i in range(3):
            record[i].append(tmp[i])
    strs = ["raw", "div 16", "shrink 3"]
    drawHistogram_3(record, "例图序号", strs, [-0.55, -0.15, -0.15])
