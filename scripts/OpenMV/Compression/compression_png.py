import cv2
import os
from helpers import *


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'
    num_list = [421802, 421802]
    record = [[]]

    for num in num_list:
        img = cv2.imread(read_path+str(num)+".bmp", 0)
        record[0].append(os.path.getsize(read_path+str(num)+".bmp"))
        for cnt in range(10):
            test_para_for_png(img, num, save_path, cnt, record, 'do_restrore')

    drawHistogram_1(record[0], 8, 6)
