import os
import math
import cv2 as cv
import numpy as np

import matplotlib.pyplot as plt


def get_img_num(directionName):
    num_list = []
    for parent, dirnames, filenames in os.walk(directionName):
        for filename in filenames:
            if filename.lower().endswith('.bmp'):
                fname1, fname2 = os.path.split(filename)
                num_list.append(str.split(fname2, '.bmp')[0])
    return num_list


def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def gaussian(x, a, m, s):
    return a*np.exp(-((x-m)/s)**2)


def func1(x, a, b, c):
    return (a*x+b)*x+c


def func2(x, a, b):
    return a*x+b


def func3(x, a1, a2, a3, m1, m2, m3, s1, s2, s3):
    return a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)


def func4(x, a0, a1, a2, a3, m1, m2, m3, s1, s2, s3, b0):
    return a0*x+b0+a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)


def func5(x, a0, a1, a2, a3, m0, m1, m2, m3, s0, s1, s2, s3):
    return a0*np.exp(-((x-m0)/s0)**2)+a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)


def get_slice(image, stepSize, windowSize):
    slice_sets = []
    for (x, y, window) in sliding_window(image, stepSize, windowSize):
        if window.shape[0] != windowSize[1] or window.shape[1] != windowSize[0]:
            continue
        slice_sets.append(image[y:y + windowSize[1], x:x + windowSize[0]])
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
    # 均方根值 反映的是有效值而不是平均值
    return math.sqrt(sum([x ** 2 for x in records]) / len(records))


def get_mse(records_real, records_predict):
    # 均方误差 估计值与真值 偏差
    if len(records_real) != len(records_predict):
        return None
    return sum([(x - y) ** 2 for x, y in zip(records_real, records_predict)]) / len(records_real)


def get_rmse(records_real, records_predict):
    # 均方根误差：是均方误差的算术平方根
    mse = get_mse(records_real, records_predict)
    if mse < 0:
        return None
    return math.sqrt(mse)


def get_mae(records_real, records_predict):
    # 平均绝对误差
    if len(records_real) != len(records_predict):
        return None
    return sum([abs(x - y) for x, y in zip(records_real, records_predict)]) / len(records_real)


def draw_zero_line():
    xdata = range(0, 160)
    plt.plot(np.array(xdata), [0 for i in xdata], 'b', label='curvefit values')


def draw_image(image):
    plt.figure()
    plt.imshow(image)
    plt.show()


def prepare_window(window_x, window_y):
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    plt.rcParams['figure.figsize'] = (window_x, window_y)


def get_maxs(image, stepSize=1):
    slice_sets = get_slice(image, stepSize, (stepSize, image.shape[0]))
    maxs = []
    for img in slice_sets:
        newvalues = img.flatten()
        newvalues = [x for x in newvalues if x > 0]
        maxs.append(get_max(newvalues))
    return maxs
