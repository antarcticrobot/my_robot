# 对一张侧墙通风口的图片，手动找到通风口中心线并绘制温度曲线

import cv2
import matplotlib.pyplot as plt
from helper import map_g_to_temp

# path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
# srcPath = path+'/raw/'
# fileName = '1325532'

path = '/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1400_tqyb0'
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
ax0 = fig.add_subplot(221)
ax0.imshow(cv2.imread('./withline.jpg', 0), 'gray')
plt.title("热成像图像")
plt.xticks([]), plt.yticks([])
plt.tight_layout()

ax1 = fig.add_subplot(222)
# tmp=img[40:41, :].flatten()
tmp = img[54:55, :].flatten()
tmp = [map_g_to_temp(x) for x in (tmp)]
ax1.plot(tmp, range(160), marker='o', label="collectList1")
plt.title("竖直中心线"), plt.xlabel(""), plt.xlabel("温度/℃")
plt.xlim([0, 40]),plt.yticks([]),plt.tight_layout()


ax2 = fig.add_subplot(223)
ax2.set_xlabel(""), ax2.set_ylabel("")
ax2.set_xticks([]), ax2.set_yticks([])

ax3 = ax2.twinx()
# tmp= img[:, 71:72].flatten()
tmp = img[:, 94:95].flatten()
tmp = [map_g_to_temp(x) for x in reversed(tmp)]
ax3.plot(range(120), tmp, marker='o', label="collectList1")
ax3.set_title("水平中心线"), ax3.set_xlabel(""), ax3.set_ylabel("温度/℃")
ax3.set_ylim([5, 35]),ax3.set_xticks([])

plt.tight_layout()
plt.plot()
plt.show()
