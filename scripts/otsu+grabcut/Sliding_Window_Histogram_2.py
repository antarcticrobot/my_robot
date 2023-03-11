# 对水平方向的切片作直方图，效果很一般

import cv2
import matplotlib.pyplot as plt
from helper import *


if __name__ == '__main__':
    image = cv2.imread('./mask/grabcut/421802_raw.bmp')

    stepSize = 5
    slice_sets = get_slice(image, stepSize, (10, 120))

    cnt = len(slice_sets)
    plt.figure()
    for cur in range(0, cnt):
        img = slice_sets[cur]
        tmp = img.flatten()
        newvalues = [x for x in tmp if x > 0]
        plt.subplot(cnt, 1, cur+1)
        # plt.hist(newvalues, 256)
        plt.hist(newvalues, bins=64, weights=[
                 1./len(newvalues)]*len(newvalues))
    plt.show()
