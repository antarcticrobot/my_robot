# coding=utf-8
import pylab
import pwlf
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from process_list_2 import cal_for_fuc_of_wall


def func(x, a, b, c):
    return b * np.power(x, a) + c

def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

def cal_curve_fit(x, y):
    popt, pcov = curve_fit(func, x, y, maxfev=800000)
    y_pred = [func(i, popt[0], popt[1], popt[2]) for i in x]
    print(popt)

    plot1 = pylab.plot(x, y, '*', label='original values')
    plot2 = pylab.plot(x, y_pred, 'r', label='fit values')
    pylab.legend(loc=3, borderaxespad=0., bbox_to_anchor=(0, 0))
    pylab.show()


if __name__ == "__main__":
    paths = []
    paths.append('/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17')
    for path in paths:
        x, y = cal_for_fuc_of_wall(path, np.max)
        loc = np.argmax(y)
        if (loc > 0):
            xleft = x[0:loc+1]
            print(xleft)
            yleft = y[0:loc+1]
            print(yleft)
            cal_curve_fit(xleft, yleft)
        if (loc < len(x)):
            xright = x[loc:]
            yright = y[loc:]
            cal_curve_fit(xright, yright)


# from scipy import optimize
# import numpy as np

# x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10 ,11, 12, 13, 14, 15], dtype=float)
# y = np.array([5, 7, 9, 11, 13, 15, 28.92, 42.81, 56.7, 70.59, 84.47, 98.36, 112.25, 126.14, 140.03])

# def piecewise_linear(x, x0, y0, k1, k2):
#     return np.piecewise(x, [x < x0], [lambda x:k1*x + y0-k1*x0, lambda x:k2*x + y0-k2*x0])

# p , e = optimize.curve_fit(piecewise_linear, x, y)
# xd = np.linspace(0, 15, 100)
# plt.plot(x, y, "o")
# plt.plot(xd, piecewise_linear(xd, *p))
# plt.show()





# # initialize piecewise linear fit with your x and y data
# my_pwlf = pwlf.PiecewiseLinFit(x, y)
# # fit the data for four line segments
# res = my_pwlf.fit(2)
# # predict for the determined points
# xHat = np.linspace(min(x), max(x), num=10000)
# yHat = my_pwlf.predict(xHat)
# # plot the results
# plt.figure()
# plt.plot(x, y, 'o')
# plt.plot(xHat, yHat, '-')
# plt.show()