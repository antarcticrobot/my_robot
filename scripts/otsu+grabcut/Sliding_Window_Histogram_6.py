# 对水平方向的切片的最大值曲线，画极大值和极小值
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


def draw_maximal_minimal(list1, window_x=8, window_y=6):
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    plt.rcParams['figure.figsize'] = (window_x, window_y)
    plt.figure()
    plt.plot(list1)
    list1 = np.array(list1)
    extrema = signal.argrelextrema(list1, np.greater, order=3)
    plt.plot(extrema[0], list1[extrema], 'o', markersize=5)
    extrema = signal.argrelextrema(list1, np.less, order=3)
    plt.plot(extrema[0], list1[extrema], 'o', markersize=5)
    plt.show()


if __name__ == '__main__':
    image = cv2.imread('./mask/grabcut/421802_raw.bmp')
    # image = cv2.blur(image,(5,5))

    stepSize = 1
    slice_sets = get_slice(image, stepSize, (1, 120))

    maxs = []
    for img in slice_sets:
        newvalues = img.flatten()
        newvalues = [x for x in newvalues if x > 0]
        maxs.append(get_max(newvalues))

    draw_maximal_minimal(maxs)
