# 对多个时间序列的墙面数据，寻找最高温度，分2段以对数曲线拟合

# coding=utf-8
import pylab
import pwlf
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from process_list_2 import cal_for_fuc_of_wall
from helper import *
from process_list_with_gap_1 import get_x_y_with_gap

def func_power(x, a, b, c):
    return a * np.power(x, b) + c


def func_log(x, a, b, c):
    return a * np.log(x+b) + c


def cal_curve_fit(x, y, func):
    popt, pcov = curve_fit(func, x, y, maxfev=800000)
    perr = np.sqrt(np.diag(pcov))

    popt_for_print=[round(each,3) for each in popt]
    print(popt_for_print)

    y_pred = [func(i, popt[0], popt[1], popt[2]) for i in x]

    mean = np.mean(y)
    ss_tot = np.sum((y - mean) ** 2)
    ss_res = np.sum((y - func(x, *popt)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    print('r_squared ', round(r_squared,3))

    return y_pred


def plot_curve(x, y, fuc):
    
    loc = np.argmax(y)

    y_pred = []
    if (loc > 0):
        xleft = x[0:loc+1]
        yleft = y[0:loc+1]
        y_pred = cal_curve_fit(xleft, yleft, fuc)
    if (loc < len(x)):
        xright = x[loc:]
        yright = y[loc:]
        y_pred2 = cal_curve_fit(xright, yright, fuc)
    pylab.plot(x, y, '*',markersize=3)
    plot2 = pylab.plot(x, y_pred+y_pred2[1:len(y_pred2)+1], 'r')
    pylab.legend(loc=3, borderaxespad=0., bbox_to_anchor=(0, 0))
    pylab.legend(('实测点', '拟合曲线'))
    pylab.xlabel('时间/s'), pylab.ylabel("温度/℃")
    pylab.plot([x[loc], x[loc]], [0, 70], 'b')

    # pylab.xlim([0, 4000]),    pylab.ylim([25, 65])
    # pylab.text(x[loc]-400, 50, '升温与降温\n阶段的分界', color='k', rotation=90.,fontsize=8)
    # pylab.xlim([0, 2000]),    pylab.ylim([25, 65])
    # pylab.text(x[loc]-200, 55, '升温与降温\n阶段的分界', color='k', rotation=90.,fontsize=8)

    pylab.xlim([0, 6000]),    pylab.ylim([0, 70])
    pylab.text(x[loc]-500, 5, '升温与降温\n阶段的分界', color='k', rotation=90.,fontsize=8)
    # pylab.xlim([0, 4000]),    pylab.ylim([0, 70])
    # pylab.text(x[loc]-400, 5, '升温与降温\n阶段的分界', color='k', rotation=90.,fontsize=8)

    # print('x[loc]',x[loc])


if __name__ == "__main__":
    paths = get_paths()
    for path in paths:
        pylab.figure(figsize=[4, 3])
        x, y = cal_for_fuc_of_wall(path, np.max)
        plot_curve(x,y, func_log)
        pylab.tight_layout()

    # pylab.figure(figsize=[4, 3])
    # x, y = get_x_y_with_gap()
    # plot_curve(x,y, func_log)
    pylab.tight_layout()
    pylab.show()
