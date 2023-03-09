import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from helpers import *

record = []


def drawHistogram_1(list1):
    # list1 = [20278/x for x in list1]
    list1 = [x/20278 for x in list1]

    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    my_fontsize = 16
    length = len(list1)
    x = np.arange(length)   # 横坐标范围
    width = 0.5

    plt.figure()
    plt.title("")
    plt.xlabel("png压缩级别", fontsize=my_fontsize)
    plt.xticks(x, ["raw", 0, 1, 2, 3, 4, 5, 6, 7, 8, 9])  # 设置x轴刻度显示值
    # plt.ylabel("结果图片大小/Byte", fontsize=my_fontsize)
    plt.ylabel("压缩比", fontsize=my_fontsize)
    # plt.ylim((0, 3.5))
    rect1 = plt.bar(x, list1, width=width, label="div")

    print_value(rect1,- 0.2)
    # for rect in rect1:
    #     height = rect.get_height()

    #     # str='%s' % (height)
    #     # str='%.3f' % (height)
    #     str = 
    #     plt.text(rect.get_x()+rect.get_width()/2. - 0.2, 1.02*height, str)
    plt.legend()
    plt.show()


def test_para_for_png(img, path_name, cnt):
    cur_name = path_name+"_"+str(cnt)+".png"
    cv2.imwrite(cur_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    record.append(size)
    print("png: ", cnt, " ", size)

    restore_name = path_name+"_"+str(cnt)+"_restore.bmp"
    cv2.imwrite(restore_name, cv2.imread(cur_name, 0))
    size = os.path.getsize(restore_name)
    print("restore.bmp: ", size)


if __name__ == '__main__':
    path_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/421802'
    save_name = './selected_pic_for_test_compression_png/output/421802'
    cur_name = path_name+".bmp"
    img = cv2.imread(cur_name, 0)

    size = os.path.getsize(cur_name)
    record.append(size)
    print("bmp: ", size)

    for cnt in range(10):
        test_para_for_png(img, save_name, cnt)
    drawHistogram_1(record)
