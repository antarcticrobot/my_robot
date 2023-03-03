# 对图像进行水平方向的切片

import cv2


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

    # 自定义滑动窗口的大小
    (winW, winH) = (10, 120)
    # 步长大小
    stepSize = 5
    cnt = 0

    
    for (x, y, window) in sliding_window(image, stepSize=stepSize, windowSize=(winW, winH)):
        if window.shape[0] != winH or window.shape[1] != winW:
            continue
        
        clone = image.copy()
        cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        cv2.imshow("Window", clone)
        cv2.waitKey(1000)

        slice = image[y:y+winH, x:x+winW]
        cv2.namedWindow('sliding_slice', 0)
        cv2.imshow('sliding_slice', slice)
        cv2.waitKey(1000)
        cnt = cnt + 1
