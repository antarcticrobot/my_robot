import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

from scipy import signal


def get_img_num(directionName, suffix='.bmp'):
    num_list = []
    for parent, dirnames, filenames in os.walk(directionName):
        for filename in filenames:
            if filename.lower().endswith(suffix):
                fname1, fname2 = os.path.split(filename)
                num_list.append(str.split(fname2, suffix)[0])
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


def prepare_window(window_x=8, window_y=6):
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    plt.rcParams['figure.figsize'] = (window_x, window_y)


def get_maxs(image, stepSize=1):
    slice_sets = get_slice(image, stepSize, (stepSize, image.shape[0]))
    maxs = []
    for img in slice_sets:
        maxs.append(np.array(img).max())
    return maxs


def get_diff(arr):
    ans = [0]
    for i in range(0, len(arr)-1):
        if (arr[i+1] >= arr[i]):
            t = arr[i+1]-arr[i]
        else:
            t = -int(arr[i]-arr[i+1])
        ans.append(t)
    return ans


def draw_without_axis_many(cnt_x, cnt_y, imgs, strs, coordinates):
    fig, axes = plt.subplots(cnt_x, cnt_y, figsize=(3*cnt_y, 3*cnt_x),
                             sharex=True, sharey=True, subplot_kw={'adjustable': 'box'})
    for i in range(cnt_x):
        for j in range(cnt_y):
            axes[i*cnt_x+j].imshow(imgs[i], cmap=plt.cm.gray)
            axes[i*cnt_x+j].set_title(strs[i])
            axes[i*cnt_x+j].axis('off')
    axes[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
    fig.tight_layout()
    plt.show()


def get_maximal_minimal(list1, result_name):
    prepare_window()

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


def get_peaks(list1, result_name):
    prepare_window()
    plt.figure()
    plt.plot(list1)
    peaks = signal.find_peaks(list1, distance=5, prominence=20)
    tmp = peaks[0]
    for ii in range(len(tmp)):
        plt.plot(tmp[ii], list1[tmp[ii]], '*', markersize=10)
    plt.savefig(result_name)
    plt.close()
    return len(tmp)


def get_para_for_test_pyg():
    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    num_list = get_img_num(read_path)
    result_path = './mask/grabcut/'
    return read_path, num_list, result_path


def get_para_for_remote_pyg():
    # 远距离拍摄，先分割
    read_path = './mask/grabcut/'
    num_list = ['421802_raw']
    return read_path, num_list


def get_para_for_near_pyg():
    # 近距离拍摄，无需分割，直接对原始图像处理
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    num_list = ['463202', '470328']
    return read_path, num_list
