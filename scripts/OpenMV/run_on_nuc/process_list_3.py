# 对多个时间序列的墙面数据，寻找最高温度，分2段以对数曲线拟合

# coding=utf-8
import pylab
import pwlf
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from process_list_2 import cal_for_fuc_of_wall
from helper import *

def func_power(x, a, b, c):
    return b * np.power(x, a) + c


def func_log(x, a, b, c):
    return b * np.log(x+a) + c


def cal_curve_fit(x, y, func):
    popt, pcov = curve_fit(func, x, y, maxfev=800000)
    y_pred = [func(i, popt[0], popt[1], popt[2]) for i in x]
    print(popt)

    plot1 = pylab.plot(x, y, '*', label='original values')
    plot2 = pylab.plot(x, y_pred, 'r', label='fit values')
    pylab.legend(loc=3, borderaxespad=0., bbox_to_anchor=(0, 0))


def plot_curve(path, fuc):
    x, y = cal_for_fuc_of_wall(path, np.max)
    loc = np.argmax(y)
    if (loc > 0):
        xleft = x[0:loc+1]
        print(xleft)
        yleft = y[0:loc+1]
        print(yleft)
        cal_curve_fit(xleft, yleft, fuc)
    if (loc < len(x)):
        xright = x[loc:]
        yright = y[loc:]
        cal_curve_fit(xright, yright, fuc)


if __name__ == "__main__":
    paths = get_paths()
    for path in paths:
        plot_curve(path, func_log)
    pylab.show()
