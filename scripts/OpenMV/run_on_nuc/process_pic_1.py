# 对一张图片的温度数据，绘制3D图再绘制等温线/直接绘制等温线

import cv2
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from helper import *


def draw_isotherm_and_3D(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_zlim(10, 40)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.invert_yaxis()
    cset = ax.contour(X, Y, Z, zdir='z', offset=10, cmap=cm.coolwarm)
    plt.show()


def draw_isotherm(X, Y, Z):
    fig = plt.figure()
    plt.contourf(X, Y, Z, 8, alpha=0.75)
    C = plt.contour(X, Y, Z, 8, colors='black')
    plt.clabel(C, inline=True, fontsize=5)
    plt.show()


path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
fileName = '1325532'
# fileName = '2438350'
img = cv2.imread(srcPath+fileName+'.pgm', 0)

X, Y = np.meshgrid(range(img.shape[1]), range(img.shape[0]))
Z = map_g_to_temp(np.array(img))

draw_isotherm_and_3D(X, Y, Z)
draw_isotherm(X, Y, Z)
