# -*- coding: utf-8 -*-

# 对指定文件夹，绘制极大值和极小值，并保存

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


def get_maximal_minimal(list1, result_name, window_x=8, window_y=6):
    prepare_window(window_x, window_y)

    plt.figure()
    list1 = np.array(list1)
    plt.plot(list1)
    extrema_1 = signal.argrelextrema(list1, np.greater, order=1)
    # plt.plot(extrema_1[0], list1[extrema_1], 'o', markersize=5)
    extrema_2 = signal.argrelextrema(list1, np.less, order=1)
    # plt.plot(extrema_2[0], list1[extrema_2], 'o', markersize=5)
    plt.savefig(result_name)
    plt.close()
    return extrema_1, extrema_2


if __name__ == '__main__':
    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    num_list = get_img_num(read_path)
    result_path = './mask/grabcut/'
    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        maxs = get_maxs(image)
        result_name = "{0}{1}_maximal_minimal.png".format(result_path, num)
        extrema_1, extrema_2 = get_maximal_minimal(maxs, result_name)
