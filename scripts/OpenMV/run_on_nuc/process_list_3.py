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
    return a * np.power(x, b) + c


def func_log(x, a, b, c):
    return a * np.log(x+b) + c


def cal_curve_fit(x, y, func):
    popt, pcov = curve_fit(func, x, y, maxfev=800000)
    perr = np.sqrt(np.diag(pcov))
    print(popt)
    print(pcov)
    print(perr)

    mean = np.mean(y)  # 1.y mean
    ss_tot = np.sum((y - mean) ** 2)  # 2.total sum of squares
    ss_res = np.sum((y - func(x, *popt)) ** 2)  # 3.residual sum of squares
    r_squared = 1 - (ss_res / ss_tot)  # 4.r squared

    print('r_squared ',r_squared)

    y_pred = [func(i, popt[0], popt[1], popt[2]) for i in x]
    return y_pred



def plot_curve(path, fuc):
    x, y = cal_for_fuc_of_wall(path, np.max)
    loc = np.argmax(y)
    
    pylab.figure(figsize=[6,4])
    y_pred=[]
    if (loc > 0):
        xleft = x[0:loc]
        # print(xleft)
        yleft = y[0:loc]
        # print(yleft)
        y_pred=cal_curve_fit(xleft, yleft, fuc)
    pylab.text(1500,5,'升温阶段',color='k'),    pylab.text(3500,5,'降温阶段',color='k')
    pylab.xlim([0,4000]),    pylab.ylim([0,70])
    if (loc < len(x)):
        xright = x[loc:]
        yright = y[loc:]
        y_pred2=cal_curve_fit(xright, yright, fuc)
    pylab.plot(x, y, '*')
    plot2 = pylab.plot(x, y_pred+y_pred2[0:len(y_pred2)+1], 'r')
    pylab.legend(loc=3, borderaxespad=0., bbox_to_anchor=(0, 0))
    pylab.legend(('实测点','拟合曲线')) 
    pylab.plot([x[loc],x[loc]],[0,70],'b')



if __name__ == "__main__":
    paths = get_paths()
    for path in paths:
        plot_curve(path, func_log)

    pylab.xlabel('时间/s')
    pylab.ylabel("温度/℃")
    pylab.show()
