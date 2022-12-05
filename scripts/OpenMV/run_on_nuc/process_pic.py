import cv2
import matplotlib.pyplot as plt
from helper import *

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np


path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
# fileName = '1325532'
fileName = '2438350'
img = cv2.imread(srcPath+fileName+'.pgm', 0)
img2 = cv2.imread(srcPath+fileName+'.pgm', 0)



fig = plt.figure()
ax = fig.gca(projection='3d')

# Make data.
X = range(160)
Y = range(120)
X, Y = np.meshgrid(X, Y)

Z = np.array(img2)
Z=map_g_to_temp(Z)
# # Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, alpha=0.5)
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
ax.invert_yaxis()

fig.colorbar(surf, shrink=0.5, aspect=5)
cset = ax.contour(X, Y, Z, zdir='z', offset=10, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='x', offset=0, cmap=cm.coolwarm)
# cset = ax.contour(X, Y, Z, zdir='y', offset=0, cmap=cm.coolwarm)
ax.set_zlim(10, 40)
 

plt.show()

# cv2.line(img2, (0, 40), (160, 40), (255, 0, 0))
# cv2.line(img2, (72, 0), (72, 120), (255, 0, 0))
# cv2.imwrite('./withline.jpg', img2)

# list1 = img[40:41, :].flatten()
# list2 = img[:, 56:57].flatten()
# fig = plt.figure()
# plt.plot(range(160), list1, marker='o', label="collectList1")
# fig = plt.figure()
# plt.plot(range(120), list2, marker='o', label="collectList1")
# plt.plot()
# plt.show()

