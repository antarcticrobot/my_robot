# -*- coding: utf-8 -*-

# 对指定文件夹，绘制极大值和极小值，并保存

import cv2
from helper import *


if __name__ == '__main__':
    read_path, num_list, result_path = get_para_for_test_pyg()

    for num in num_list:
        image = cv2.imread(read_path+str(num)+".bmp")
        
        maxs = get_maxs(image)
        result_name = "{0}{1}_maximal_minimal.png".format(result_path, num)
        extrema_1, extrema_2 = get_maximal_minimal(maxs, result_name)
