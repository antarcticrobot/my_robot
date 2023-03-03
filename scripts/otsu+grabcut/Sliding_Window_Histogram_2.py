# 对水平方向的切片作直方图，效果很一般

import cv2
import matplotlib.pyplot as plt
import numpy as np


def sliding_window(image, stepSize, windowSize):
    for y in range(0, image.shape[0], stepSize):
        for x in range(0, image.shape[1], stepSize):
            yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def get_slice(image, stepSize, windowSize):
    slice_sets = []
    for (x, y, window) in sliding_window(image, stepSize, windowSize):
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        slice = image[y:y + winH, x:x + winW]
        slice_sets.append(slice)
    return slice_sets



if __name__ == '__main__':
    image = cv2.imread('./mask/grabcut/421802_raw.bmp')

    (winW, winH) = (10, 120)
    stepSize = 5
    slice_sets = get_slice(image, stepSize, (winW, winH))

    cnt = len(slice_sets)

    plt.figure()

    average=[]
    variance=[]
    std_deviation=[]
    rms=[]


    for cur in range(0, cnt):
        img = slice_sets[cur]

        tmp = img.flatten()
        newvalues = [x for x in tmp if x > 0]

        plt.subplot(cnt, 1, cur+1)
        # plt.hist(newvalues, 256)
        plt.hist(newvalues,bins=64,weights=[1./len(newvalues)]*len(newvalues))


    plt.show()
