# 对比了bmp与jpg的效果
# 虽然还没找到办法用算法标注出破损位置，视觉上够明显了

import cv2
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


def draw_isotherm_and_3D(X, Y, Z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
    ax.invert_yaxis()
    cset = ax.contour(X, Y, Z, zdir='z', offset=10, cmap=cm.coolwarm)
    plt.show()


def draw_isotherm(X, Y, Z):
    fig = plt.figure()
    countours = plt.contourf(X, Y, Z, 60, alpha=0.75)
    
    # print(countours.collections[0].get_paths())
    # temp = countours.collections[0].get_paths()
    # xy = []
    # for vv in temp:
    #     xy.append(vv)
    # print(xy)

    cset = plt.contour(X, Y, Z, 60, colors='black')
    print(cset)

    plt.xlabel("Pixel abscissa")
    plt.ylabel("Pixel ordinate")
    plt.show()
    return temp


# path = './mask/grabcut/421802_raw.jpg'
path = './mask/grabcut/421802_raw.bmp'

img = cv2.imread(path, 0)
img = cv2.flip(img, 0, dst=None)
img=cv2.blur(img,(3,3))

X, Y = np.meshgrid(range(img.shape[1]), range(img.shape[0]))
# temp = draw_isotherm_and_3D(X, Y, img)
temp = draw_isotherm(X, Y, img)
