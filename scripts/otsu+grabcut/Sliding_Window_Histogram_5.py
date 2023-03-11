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
    plt.imshow(image)
    plt.show()

    plt.figure()
    plt.plot(list1)

    # peaks = signal.find_peaks(list1, height=180)
    peaks = signal.find_peaks(list1, distance=5, prominence=15)
    for ii in range(len(peaks[0])):
        plt.plot(peaks[0][ii],
                 list1[peaks[0][ii]], '*', markersize=10)

    # plt.plot(max_diff)
    # xdata=range(0,160)
    # plt.plot(np.array(xdata), [0 for i in xdata], 'b', label='curvefit values')

    # list1 = np.array(list1)
    # extrema = signal.argrelextrema(list1, np.greater)
    # plt.plot(extrema[0], list1[extrema], 'o', markersize=5)
    # extrema = signal.argrelextrema(list1, np.less)
    # plt.plot(extrema[0], list1[extrema], 'o', markersize=5)
    plt.show()


if __name__ == '__main__':
    # image = cv2.imread('./mask/grabcut/421802_raw.bmp')
    image = cv2.imread(
        "/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/463202.bmp", 0)
    # image = cv2.imread(
    #     "/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/470328.bmp", 0)


    # image = cv2.blur(image,(5,5))

    stepSize = 1
    slice_sets = get_slice(image, stepSize, (1, 120))

    maxs = []
    for img in slice_sets:
        newvalues = img.flatten()
        newvalues = [x for x in newvalues if x > 0]
        maxs.append(get_max(newvalues))

    max_diff = [0]
    for i in range(0, 159):
        if (maxs[i+1] >= maxs[i]):
            t = maxs[i+1]-maxs[i]
        else:
            t = -int(maxs[i]-maxs[i+1])
        max_diff.append(t)

    draw_maximal_minimal(maxs)
    draw_maximal_minimal(max_diff)
