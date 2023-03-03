import cv2 as cv
import matplotlib.pyplot as plt
# 1. 图像读取
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1882626.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1884624.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1824640.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/2236399.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/2426441.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/1393595.jpg', 0)
# img = cv.imread('/home/yr/热成像数据_存档_排烟管/2023_02_20_1630_pyg/raw/444743.jpg', 0)
img = cv.imread('/home/yr/热成像数据_存档_排烟管/2023_02_20_1630_pyg/raw/421802.bmp', 0)

# img = cv.imread('/home/yr/热成像数据_存档_排烟管/2023_02_20_1620_pyg/raw/444378.bmp',0)


# 2.固定阈值 threshold(要处理的图像，一般是灰度图, 设定的阈值, 灰度中的最大值, 阈值分割的方式)
ret, th1 = cv.threshold(img, 110, 255, cv.THRESH_BINARY)
ret, th1_2 = cv.threshold(img, 120, 255, cv.THRESH_BINARY)
ret, th1_3 = cv.threshold(img, 130, 255, cv.THRESH_BINARY)
# 3. OSTU阈值 threshold(要处理的图像，一般是灰度图, 设定的阈值, 灰度中的最大值, 阈值分割的方式)
# img = cv.imread('/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw/2426441.jpg', 0)
th2 = cv.adaptiveThreshold(
    img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, 0)

ret2, th3 = cv.threshold(img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

cv.imwrite("./mask/421802.bmp", th3)

# 4. 结果绘制
# plt.figure(figsize=(10,8),dpi=200, facecolor='white')
plt.subplot(231), plt.imshow(img, 'gray'), plt.title('Original Imgae')
plt.subplot(232), plt.imshow(th2, 'gray'), plt.title(
    'Adaptive Threshold Segmentation')
plt.subplot(233), plt.imshow(th3, 'gray'), plt.title('OStu segmentation')

plt.subplot(234), plt.imshow(th1, 'gray'), plt.title('Fixed Threshold = 110')
plt.subplot(235), plt.imshow(th1_2, 'gray'), plt.title('Fixed Threshold = 120')
plt.subplot(236), plt.imshow(th1_3, 'gray'), plt.title('Fixed Threshold = 130')
plt.show()
