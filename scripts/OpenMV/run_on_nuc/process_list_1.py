# 对一个时间序列的侧墙通风口数据，寻找代表通风口的矩形，并计算与通风口等宽的竖直条中，其上、其中、其下三块的平均温度或其他

import cv2
import matplotlib.pyplot as plt
from helper import *


def cal_for_up_mid_down_of_vent(img, x, y, w, h, fuc):
    if (h <= 0):
        return None, None, None
    if (x > 0):
        tmpArr = img[y:y+h, 0:x]
        ans1 = map_g_to_temp(fuc(tmpArr))
    else:
        ans1 = None
    if (w > 0):
        tmpArr = img[y:y+h, x:x+w]
        ans2 = map_g_to_temp(fuc(tmpArr))
    else:
        ans2 = None
    if (x+w < 120):
        tmpArr = img[y:y+h, x+w:120]
        ans3 = map_g_to_temp(fuc(tmpArr))
    else:
        ans3 = None
    return ans1, ans2, ans3


def ShapeDetection(img, imgContour, lists):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    maxArea = -1
    loc = -1
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if (maxArea < area):
            maxArea = area
            loc = i

    if (loc > -1):
        obj = contours[loc]
        perimeter = cv2.arcLength(obj, True)
        approx = cv2.approxPolyDP(obj, 0.02*perimeter, True)
        CornerNum = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
        objType = get_shape_name(CornerNum, w, h)

        ans = cal_for_up_mid_down_of_vent(imgContour, x, y, w, h, np.mean)
        lists.append(ans)

        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(imgContour, objType, (x+(w//2), y+(h//2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        print(CornerNum, area)
    else:
        lists.append([0, 0, 0])


def process_img(srcPath, dstPath, fileName, lists):
    imgGray = cv2.imread(srcPath+fileName+'.pgm', 0)
    imgContour = imgGray.copy()
    ret, imgBinary = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    conv_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    imgDilate = cv2.dilate(imgBinary, conv_kernel)
    imgErod = cv2.erode(imgDilate, conv_kernel)
    imgCanny = cv2.Canny(imgErod, 60, 60)
    ShapeDetection(imgCanny, imgContour, lists)

    cv2.imwrite(midPath+fileName+'_Gray.jpg', imgGray)
    cv2.imwrite(midPath+fileName+'_Binary.jpg', imgBinary)
    cv2.imwrite(midPath+fileName+'_Dilate.jpg', imgDilate)
    cv2.imwrite(midPath+fileName+'_Erod.jpg', imgErod)
    cv2.imwrite(midPath+fileName+'_Canny.jpg', imgCanny)
    cv2.imwrite(dstPath+fileName+'_Contour.jpg', imgContour)


if __name__ == "__main__":
    path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
    srcPath, midPath, dstPath = get_full_paths(path)
    listName = './img_lists/2022_11_28_1100_tqyb17/vent.txt'

    collectLists = []
    fp = open(listName, 'r')
    filenames = [each.rstrip('\r\n') for each in fp.readlines()]
    for fileName in filenames:
        process_img(srcPath, dstPath, fileName, collectLists)

    fig = plt.figure(figsize=(4, 4), dpi=300)
    x_lable = [int(each)/1000 for each in filenames]
    collectLists = np.array(collectLists)

    plt.plot(x_lable, collectLists[:, 0].flatten(), marker='o', label="up")
    plt.plot(x_lable, collectLists[:, 1].flatten(), marker='D', label="target")
    plt.plot(x_lable, collectLists[:, 2].flatten(), marker='*', label="below")
    plt.xlabel('time')
    plt.ylabel('temperature')
    plt.xticks(np.arange(0, 4800, 1000))
    plt.yticks(np.arange(20, 36, 1))
    plt.show()
