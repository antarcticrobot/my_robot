import cv2
import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from helper import *

path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
# fileName = '1325532'
fileName = '2438350'
img = cv2.imread(srcPath+fileName+'.pgm', 0)

X = range(160)
Y = range(120)
X, Y = np.meshgrid(X, Y)
Z = np.array(img)
Z = map_g_to_temp(Z)

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
ax.set_zlim(10, 40)
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.invert_yaxis()
fig.colorbar(surf, shrink=0.5, aspect=5)
cset = ax.contour(X, Y, Z, zdir='z', offset=10, cmap=cm.coolwarm)
plt.show()
