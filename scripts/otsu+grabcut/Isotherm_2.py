# 对一张图片的温度数据，绘制3D图再绘制等温线/直接绘制等温线

import cv2
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
# from helper import *


def draw_isotherm_and_3D(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.set_zlim(10, 40)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.invert_yaxis()
    cset = ax.contour(X, Y, Z, zdir='z', offset=10, cmap=cm.coolwarm)
    # for tmp in cset:
    #     print(tmp)
    plt.show()


def draw_isotherm(X, Y, Z):
    fig = plt.figure()
    countours = plt.contourf(X, Y, Z, 8, alpha=0.75)
    # for tmp in countours:
    print(countours)
    cset = plt.contour(X, Y, Z, 8, colors='black')
    plt.clabel(cset, inline=True, fontsize=5)
    # listTmp= cset.collections
    # for cur in listTmp:
    #     print(cur.Lines)
    plt.xlabel("Pixel abscissa")
    plt.ylabel("Pixel ordinate")
    plt.show()


path = './mask/grabcut/421802_raw.bmp'
# srcPath = path+'/raw/'
# fileName = '1325532'
fileName = '2438350'
img = cv2.imread(path, 0)
img=cv2.flip(img,0,dst=None)

X, Y = np.meshgrid(range(img.shape[1]), range(img.shape[0]))
Z = img#map_g_to_temp(np.array(img))
# draw_isotherm_and_3D(X, Y, Z)
draw_isotherm(X, Y, Z)

# plt.imshow(cv2.Laplacian(img,cv2.CV_64F),cmap='gray')
# plt.title('Opencv')
# plt.show()