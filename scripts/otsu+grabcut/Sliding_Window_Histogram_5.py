# -*- coding: utf-8 -*-

# 对指定文件夹，绘制峰值
# 近距离拍摄，无需分割，直接对原始图像处理
# 远距离拍摄，先分割

import cv2
import matplotlib.pyplot as plt
from scipy import signal
from helper import *


if __name__ == '__main__':
    # read_path, num_list = get_para_for_near_pyg()
    # read_path, num_list = get_para_for_remote_pyg()
    read_path, num_list, result_path = get_para_for_test_pyg()

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        
        maxs = get_maxs(image)
        result_name = "{0}{1}_peek.png".format(result_path, num)
        peaks_num = get_peaks(maxs, result_name)
        # print('{0}.bmp 有{1}个疑似破损点'.format(num, peaks_num))

        max_diff = get_diff(maxs)
        result_name = "{0}{1}_diff_peek.png".format(result_path, num)
        get_peaks(max_diff, result_name)
