# 对一张侧墙的图片，计算梯度的最大值和均值——看起来也解释不通

import cv2
import numpy as np
import matplotlib.pyplot as plt
import time


def Sobel(img, filter1, filter2):
    h, w = img.shape[:2]
    new_img = np.zeros((h+2, w+2), np.uint8)
    new_img[1:h+1, 1:w+1] = img  # 填充
    out = []
    for i in range(1, h+1):
        for j in range(1, w+1):
            dx = np.sum(np.multiply(new_img[i-1:i+2, j-1:j+2], filter1))
            dy = np.sum(np.multiply(new_img[i-1:i+2, j-1:j+2], filter2))
            # out.append(np.clip(int(np.sqrt(dx**2+dy**2)), 0, 255))
            out.append(int(np.sqrt(dx**2+dy**2)))
    out = np.array(out).reshape(h, w)
    return out


if __name__ == "__main__":

    path = '/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1400_tqyb0'
    srcPath = path+'/raw/'
    # fileName = '2991805'
    # fileName = '3014868'
    fileName = '1348297'
    # fileName = '1385475'
    # fileName = '1363976'
    # fileName = '792471'


    img = cv2.imread(srcPath+fileName+'.pgm', 0)

    filter1 = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    filter2 = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    plt.figure(figsize=(6, 8))
    plt.subplot(121)
    out= Sobel(img, filter1, filter2)
    print(np.max(out))
    print(np.mean(out))
    plt.imshow(out, cmap='gray')
    plt.subplot(122)
    plt.imshow(cv2.Laplacian(img,cv2.CV_64F),cmap='gray')

    plt.show()
