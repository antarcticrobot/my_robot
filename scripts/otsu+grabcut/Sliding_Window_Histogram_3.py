# 对水平方向的切片作方差等统计值的变化曲线，效果很一般
# 直接统计最大值,效果很好

# # -*- coding: utf-8 -*-

import math
import cv2
import matplotlib.pyplot as plt
import numpy as np


def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def get_slice(image, stepSize, windowSize):
    slice_sets = []
    for (x, y, window) in sliding_window(image, stepSize, windowSize):
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        slice = image[y:y + winH, x:x + winW]
        slice_sets.append(slice)
    return slice_sets


def get_max(records):
    return max(records)

def get_average(records):
    return sum(records) / len(records)


def get_variance(records):
    average = get_average(records)
    return sum([(x - average) ** 2 for x in records]) / len(records)


def get_standard_deviation(records):
    variance = get_variance(records)
    return math.sqrt(variance)


def get_rms(records):
    """
    均方根值 反映的是有效值而不是平均值
    """
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))


def get_mse(records_real, records_predict):
    """
    均方误差 估计值与真值 偏差
    """
    if len(records_real) == len(records_predict):
        return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None


def get_rmse(records_real, records_predict):
    """
    均方根误差：是均方误差的算术平方根
    """
    mse = get_mse(records_real, records_predict)
    if mse:
        return math.sqrt(mse)
    else:
        return None


def get_mae(records_real, records_predict):
    """
    平均绝对误差
    """
    if len(records_real) == len(records_predict):
        return sum([abs(x - y) for x, y in zip(records_real, records_predict)]) / len(records_real)
    else:
        return None


if __name__ == '__main__':
    image = cv2.imread('./mask/grabcut/421802_raw.bmp')
    image = cv2.blur(image,(3,3))
    (winW, winH) = (1, 120)
    stepSize = 1
    slice_sets = get_slice(image, stepSize, (winW, winH))

    cnt = len(slice_sets)

    plt.figure()

    maxs=[]
    average = []
    variance = []
    std_deviation = []
    rms = []

    for cur in range(0, cnt):
        img = slice_sets[cur]

        tmp = img.flatten()
        newvalues = [x for x in tmp if x > 0]

        # plt.subplot(cnt, 1, cur+1)
        # plt.hist(newvalues, 256)

        max1=get_max(newvalues)
        maxs.append(max1)
        average1 = get_average(newvalues)
        average.append(average1)
        variance1 = get_variance(newvalues)
        variance.append(variance1)
        std_deviation1 = get_standard_deviation(newvalues)
        std_deviation.append(std_deviation1)
        rms1 = get_rms(newvalues)
        rms.append(rms1)

    plt.subplot(1, 1, 1)
    plt.plot(maxs)
    
    plt.ylim(120,240)
    # plt.subplot(5, 1, 2)
    # plt.plot(average)
    # plt.subplot(5, 1, 3)
    # plt.plot(variance)
    # plt.subplot(5, 1, 4)
    # plt.plot(std_deviation)
    # plt.subplot(5, 1, 5)
    # plt.plot(rms)

    plt.show()
