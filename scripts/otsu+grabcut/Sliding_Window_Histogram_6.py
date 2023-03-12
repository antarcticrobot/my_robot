# 对水平方向的切片的最大值曲线，画极大值和极小值
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


def get_maximal_minimal(list1, window_x=8, window_y=6):
    prepare_window(window_x, window_y)

    plt.figure()
    list1 = np.array(list1)
    plt.plot(list1)
    extrema_1 = signal.argrelextrema(list1, np.greater, order=1)
    plt.plot(extrema_1[0], list1[extrema_1], 'o', markersize=5)
    extrema_2 = signal.argrelextrema(list1, np.less, order=1)
    plt.plot(extrema_2[0], list1[extrema_2], 'o', markersize=5)
    plt.show()
    return extrema_1,extrema_2


if __name__ == '__main__':
    # read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    # num_list = ['463202', '470328']
    read_path = './mask/grabcut/'
    num_list = ['421802_raw']

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        # draw_image(image)
        # image = cv2.blur(image, (3, 3))

        maxs = get_maxs(image)
        extrema_1,extrema_2= get_maximal_minimal(maxs)
