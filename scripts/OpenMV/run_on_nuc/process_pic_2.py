# 对一张侧墙通风口的图片，手动找到通风口中心线并绘制温度曲线

import cv2
import matplotlib.pyplot as plt
from helper import map_g_to_temp

# path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
# srcPath = path+'/raw/'
# fileName = '1325532'

path = '/home/yr/热成像数据_存档/2022_11_30_1400_tqyb0'
srcPath = path+'/raw/'
fileName = '3875510'

img = cv2.imread(srcPath+fileName+'.pgm', 0)
img2 = cv2.imread(srcPath+fileName+'.pgm', 0)
# cv2.line(img2, (0, 40), (160, 40), (255, 0, 0))
# cv2.line(img2, (72, 0), (72, 120), (255, 0, 0))

cv2.line(img2, (0, 54), (160, 54), (255, 0, 0))
cv2.line(img2, (94, 0), (94, 120), (255, 0, 0))

cv2.imwrite('./withline.jpg', img2)

fig = plt.figure()

ax1 = fig.add_subplot(121)
# tmp=img[40:41, :].flatten()
tmp=img[54:55, :].flatten()
tmp= [map_g_to_temp(x) for x in (tmp)]
ax1.plot(range(160), tmp, marker='o', label="collectList1")
plt.title("Vertical center line")
plt.xlabel("Pixel ordinate")
plt.ylabel("Temperature/℃")


ax2 = fig.add_subplot(122)
# tmp= img[:, 71:72].flatten()
tmp= img[:, 94:95].flatten()
tmp= [map_g_to_temp(x) for x in reversed(tmp)]
ax2.plot(range(120), tmp, marker='o', label="collectList1")
plt.title("Horizontal center line")
plt.xlabel("Pixel abscissa")
plt.ylabel("Temperature/℃")






plt.plot()
plt.show()
