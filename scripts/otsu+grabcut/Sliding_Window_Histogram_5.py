# 对水平方向的切片的最大值曲线，画极大值和极小值

# -*- coding: utf-8 -*-

import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy import signal 

def gaussian(x,a,m,s):
      return a*np.exp(-((x-m)/s)**2)
      
def func1(x,a,b,c):
      return (a*x+b)*x+c
def func2(x,a,b):
      return a*x+b

def func3(x,a1,a2,a3,m1,m2,m3,s1,s2,s3):
      return a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)

def func4(x,a0,a1,a2,a3,m1,m2,m3,s1,s2,s3,b0):
      return a0*x+b0+a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)

def func5(x,a0,a1,a2,a3,m0,m1,m2,m3,s0,s1,s2,s3):
      return a0*np.exp(-((x-m0)/s0)**2)+a1*np.exp(-((x-m1)/s1)**2)+a2*np.exp(-((x-m2)/s2)**2)+a3*np.exp(-((x-m3)/s3)**2)


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
    # image = cv2.blur(image,(5,5))
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

    max_diff=[]
    max_diff.append(0)
    for i in range(0,159):
        if(maxs[i+1]>maxs[i]):
            t=maxs[i+1]-maxs[i]
        else:
            t=maxs[i]-maxs[i+1]
            t=int(t)
            t=-t
        print(type(t))
        print(t," ",maxs[i+1]," ",maxs[i])
        max_diff.append(t)

    plt.subplot(1, 1, 1)

    # num_peak_3 = signal.find_peaks(maxs, distance=1)
    # for ii in range(len(num_peak_3[0])):
    #     plt.plot(num_peak_3[0][ii], maxs[num_peak_3[0][ii]],'*',markersize=10)
    yvals=np.array(maxs)
    plt.plot(signal.argrelextrema(yvals,np.greater)[0],yvals[signal.argrelextrema(yvals, np.greater)],'o', markersize=10)  #极大值点
    plt.plot(signal.argrelextrema(yvals,np.less)[0],yvals[signal.argrelextrema(yvals, np.less)],'o', markersize=10)  #极小值点


    plt.plot(maxs)
    # plt.plot(max_diff)
    # xdata=range(0,160)
    # plt.plot(np.array(xdata), [0 for i in xdata], 'b', label='curvefit values')

    # plt.ylim(120,240)


    # xdata= range(2,13)
    # popt, pcov = curve_fit(func1, xdata, maxs[2:13],maxfev=40000)
    # plot2 = plt.plot(np.array(xdata), [func1(i, *popt) for i in xdata], 'b', label='curvefit values')

    # xdata= range(13,23)
    # popt, pcov = curve_fit(func1, xdata, maxs[13:23],maxfev=40000)
    # plot2 = plt.plot(np.array(xdata), [func1(i, *popt) for i in xdata], 'b', label='curvefit values')

    # xdata= range(23,33)
    # popt, pcov = curve_fit(func1, xdata, maxs[23:33],maxfev=40000)
    # plot2 = plt.plot(np.array(xdata), [func1(i, *popt) for i in xdata], 'b', label='curvefit values')

    # xdata= range(33,146)
    # popt, pcov = curve_fit(func1, xdata, maxs[33:146],maxfev=40000)
    # plot2 = plt.plot(np.array(xdata), [func1(i, *popt) for i in xdata], 'b', label='curvefit values')


    # # xdata= range(0,150)
    # # popt, pcov = curve_fit(func4, xdata, maxs[:150],maxfev=40000)
    # # plot2 = plt.plot(np.array(xdata), [func4(i, *popt) for i in xdata], 'b', label='curvefit values')


    
    # # plt.subplot(5, 1, 2)
    # # plt.plot(average)
    # # plt.subplot(5, 1, 3)
    # # plt.plot(variance)
    # # plt.subplot(5, 1, 4)
    # # plt.plot(std_deviation)
    # # plt.subplot(5, 1, 5)
    # # plt.plot(rms)

    plt.show()
