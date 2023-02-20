import cv2 as cv
import matplotlib.pyplot as plt
# 1. 图像读取
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1882626.jpg', 0)
img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1884624.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1824640.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/2236399.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/2426441.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1393595.jpg', 0)


# 2.固定阈值 threshold(要处理的图像，一般是灰度图, 设定的阈值, 灰度中的最大值, 阈值分割的方式)
ret, th1 = cv.threshold(img, 12,255, cv.THRESH_BINARY)
# 3. OSTU阈值 threshold(要处理的图像，一般是灰度图, 设定的阈值, 灰度中的最大值, 阈值分割的方式)
ret2,th2 = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

cv.imwrite("./mask/1884624.jpg",th2)

# 4. 结果绘制
plt.figure(figsize=(10,8),dpi=200, facecolor='white')
plt.subplot(131),plt.imshow(img,'gray'),plt.title('Original imgae')
# plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(th1,'gray'),plt.title('Fixed threshold segmentation')
plt.subplot(133),plt.imshow(th2,'gray'),plt.title('OStu segmentation')
plt.show()
