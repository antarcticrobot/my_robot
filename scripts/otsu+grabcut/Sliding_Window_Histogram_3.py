# 对水平方向的切片作方差等统计值的变化曲线，效果很一般
# 直接统计最大值,效果很好
# # -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from helper import *


if __name__ == '__main__':
    image = cv2.imread('./mask/grabcut/421802_raw.bmp')
    image = cv2.blur(image, (3, 3))
    stepSize = 1
    slice_sets = get_slice(image, stepSize, (1, 120))

    maxs = get_maxs(image)
    average = []
    variance = []
    std_deviation = []
    rms = []

    for img in slice_sets:
        tmp = img.flatten()
        newvalues = [x for x in tmp if x > 0]
        average.append(get_average(newvalues))
        variance.append(get_variance(newvalues))
        std_deviation.append(get_standard_deviation(newvalues))
        rms.append(get_rms(newvalues))

    plt.figure()
    plt.subplot(5, 1, 1)
    plt.plot(maxs)
    plt.subplot(5, 1, 2)
    plt.plot(average)
    plt.subplot(5, 1, 3)
    plt.plot(variance)
    plt.subplot(5, 1, 4)
    plt.plot(std_deviation)
    plt.subplot(5, 1, 5)
    plt.plot(rms)
    plt.show()
