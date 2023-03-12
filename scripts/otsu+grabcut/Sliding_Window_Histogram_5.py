# 对水平方向的切片的最大值曲线，画极大值和极小值
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


def get_maximal_minimal(list1, window_x=8, window_y=6):
    prepare_window(window_x, window_y)
    plt.figure()
    plt.plot(list1)
    peaks = signal.find_peaks(list1, distance=5, prominence=20)
    for ii in range(len(peaks[0])):
        plt.plot(peaks[0][ii],
                 list1[peaks[0][ii]], '*', markersize=10)
    plt.show()
    return len(peaks[0])


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    num_list = ['463202', '470328']
    # read_path = './mask/grabcut/'
    # num_list = ['421802_raw']

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        draw_image(image)
        # image = cv2.blur(image,(5,5))

        maxs = get_maxs(image)
        max_diff = [0]
        for i in range(0, 159):
            if (maxs[i+1] >= maxs[i]):
                t = maxs[i+1]-maxs[i]
            else:
                t = -int(maxs[i]-maxs[i+1])
            max_diff.append(t)

        peaks_num=get_maximal_minimal(maxs)
        print('{0}.bmp 有{1}个疑似破损点'.format(num,peaks_num))
        # draw_maximal_minimal(max_diff)
