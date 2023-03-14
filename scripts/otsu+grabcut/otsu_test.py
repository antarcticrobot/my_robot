import os
import cv2 as cv
import matplotlib.pyplot as plt
from helper import *


def get_mask(bmp_name):
    img = cv.imread(bmp_name, 0)
    th1 = list((img, img, img))
    for i in range(3):
        ret, th1[i] = cv.threshold(img, 110+i*10, 255, cv.THRESH_BINARY)

    th2 = cv.adaptiveThreshold(
        img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 3, 0)

    ret2, th3 = cv.threshold(img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)

    cv.imwrite("./mask/"+str(num)+".bmp", th3)
    plt.subplot(231), plt.imshow(img, 'gray'), plt.title('原始图像')
    plt.subplot(232), plt.imshow(th2, 'gray'), plt.title('自适应阈值分割')
    plt.subplot(233), plt.imshow(th3, 'gray'), plt.title('OStu阈值分割')
    for i in range(3):
        plt.subplot(
            2, 3, 4+i), plt.imshow(th1[i], 'gray'), plt.title('固定阈值='+str(110+i*10))
    plt.show()


if __name__ == '__main__':
    # read_path = '/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/raw'
    # num_list = [1882626, 1884624, 1824640, 2236399, 2426441, 1393595]

    # read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    # num_list = [421802, 444743]

    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    num_list = get_img_num(read_path)
    for num in num_list:
        get_mask(read_path+str(num)+".bmp")
