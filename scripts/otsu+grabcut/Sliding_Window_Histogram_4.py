# 对水平方向的切片的最大值曲线，人工分段作拟合
# # -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from helper import *


if __name__ == '__main__':
    read_path, num_list = get_para_for_remote_pyg()

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        # image = cv2.blur(image,(3,3))

        stepSize = 1
        slice_sets = get_slice(image, stepSize, (1, 120))
        maxs = get_maxs(image)

        # get_maximal_minimal(maxs, '/home/yr/2023_0414/排烟管_最高温度点_带标记.png')
        # get_maximal_minimal(maxs, '/home/yr/2023_0414/排烟管_最高温度点_带标记_blur5.png')
        get_maximal_minimal(maxs, '/home/yr/2023_0414/排烟管_最高温度点_blur3.png')


        plt.figure(figsize=[4,3])
        plt.plot(maxs)
        plt.ylabel('最高温度点的灰度值'),    plt.xlabel('垂直切片位置')
        plt.ylim([120,220]),    plt.xlim([0,160])
        plt.tight_layout()
        plt.show()
