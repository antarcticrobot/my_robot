# 对近距离拍摄，未作分割的图像，已知破损数目的情况下，可精准定位——可以结合前面极大极小值的方法，确认数目后进行定位

import cv2
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from helper import *


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    num_list = [463202, 470328, 489938]
    for num in num_list:
        im = cv2.imread(read_path+str(num)+".bmp", 0)
        # im = im[:, 0:50]
        image_max = ndi.maximum_filter(im, size=12, mode='constant')
        coordinates = peak_local_max(im, min_distance=5, num_peaks=4)

        imgs = [im, image_max, im]
        strs = ['Original', 'Maximum filter', 'Peak local max']
        draw_without_axis_many(1, 3, imgs, strs, coordinates)
