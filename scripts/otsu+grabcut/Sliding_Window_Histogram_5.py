# -*- coding: utf-8 -*-

# 对指定文件夹，绘制峰值
# 近距离拍摄，无需分割，直接对原始图像处理
# 远距离拍摄，先分割

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


def get_peaks(list1, result_name, window_x=8, window_y=6):
    prepare_window(window_x, window_y)
    plt.figure()
    plt.plot(list1)
    peaks = signal.find_peaks(list1, distance=5, prominence=20)
    tmp = peaks[0]
    for ii in range(len(tmp)):
        plt.plot(tmp[ii], list1[tmp[ii]], '*', markersize=10)
    plt.savefig(result_name)
    plt.close()
    return len(tmp)


if __name__ == '__main__':
    # # 近距离拍摄，无需分割，直接对原始图像处理
    # read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    # num_list = ['463202', '470328']

    # # 远距离拍摄，先分割
    # read_path = './mask/grabcut/'
    # num_list = ['421802_raw']

    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    num_list = get_img_num(read_path)
    result_path = './mask/grabcut/'

    print(num_list)
    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")

        maxs = get_maxs(image)
        result_name = "{0}{1}_peek.png".format(result_path, num)
        peaks_num = get_peaks(maxs, result_name)
        # print('{0}.bmp 有{1}个疑似破损点'.format(num, peaks_num))

        max_diff = get_diff(maxs)
        result_name = "{0}{1}_diff_peek.png".format(result_path, num)
        get_peaks(max_diff, result_name)
