# 对水平方向的切片的最大值曲线，人工分段作拟合
# # -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from helper import *


if __name__ == '__main__':
    read_path, num_list = get_para_for_remote_pyg()

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        # image = cv2.blur(image,(5,5))

        stepSize = 1
        slice_sets = get_slice(image, stepSize, (1, 120))
        maxs = get_maxs(image)

        plt.figure()
        plt.subplot(1, 1, 1)
        plt.plot(maxs)
        str_name = 'curvefit values'

        xdata = np.array(range(2, 13))
        popt, pcov = curve_fit(func1, xdata, maxs[2:13], maxfev=40000)
        plt.plot(xdata, [func1(i, *popt) for i in xdata], 'b', label=str_name)
        xdata = np.array(range(13, 23))
        popt, pcov = curve_fit(func1, xdata, maxs[13:23], maxfev=40000)
        plt.plot(xdata, [func1(i, *popt) for i in xdata], 'b', label=str_name)
        xdata = np.array(range(23, 33))
        popt, pcov = curve_fit(func1, xdata, maxs[23:33], maxfev=40000)
        plt.plot(xdata, [func1(i, *popt) for i in xdata], 'b', label=str_name)
        xdata = np.array(range(33, 146))
        popt, pcov = curve_fit(func1, xdata, maxs[33:146], maxfev=40000)
        plt.plot(xdata, [func1(i, *popt) for i in xdata], 'b', label=str_name)

        # xdata= range(0,150)
        # popt, pcov = curve_fit(func4, xdata, maxs[:150],maxfev=40000)
        # plt.plot(xdata, [func4(i, *popt) for i in xdata], 'b', label=str_name)

        plt.show()
