import cv2
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from helpers import *
from matplotlib.ticker import FuncFormatter


record = []
for i in range(11):
    record.append([])


def drawHistogram_1(list1, window_x=8, window_y=6):
    prepare_window(window_x, window_y)
    my_fontsize = 16
    width = 0.5
    x = np.arange(len(list1))   # 横坐标范围

    list1 = np.array(list1).mean(axis=1)
    list1 = [x/20278 for x in list1]


    plt.figure()
    plt.xlabel("png压缩级别", fontsize=my_fontsize)
    plt.xticks(x, ["raw", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # 设置x轴刻度显示值
    rect1 = plt.bar(x, list1, width=width)
    # plt.ylabel("压缩率均值/%", fontsize=my_fontsize)
    plt.ylabel("压缩率标准差/%", fontsize=my_fontsize)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    print_percentage(rect1, - 0.55)
    plt.legend()
    plt.show()


def test_para_for_png(img, num, save_path, cnt):
    save_name = save_path+str(cnt)+'/'+str(num)+'.png'
    # cv2.imwrite(save_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(save_name)
    record[cnt+1].append(size)
    # print("png: ", cnt, " ", size)

    # restore_name = save_name+"_"+str(cnt)+"_restore.bmp"
    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0))
    # print_size("restore.bmp: ", restore_name)


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/for_compression/2023_02_20_1630_pyg_raw_bmp/'
    save_path = '/home/yr/热成像数据_存档_排烟管/for_compression/output/'
    num_list = get_img_num(read_path)
    print(num_list)

    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        img = cv2.imread(bmp_name, 0)
        cv2.imshow('img', img)
        # cv2.waitKey()
        size = os.path.getsize(bmp_name)
        record[0].append(size)
        # print("bmp: ", size)

        for cnt in range(10):
            test_para_for_png(img, num, save_path, cnt)
    print(record[2])

    drawHistogram_1(record, 8, 6)
