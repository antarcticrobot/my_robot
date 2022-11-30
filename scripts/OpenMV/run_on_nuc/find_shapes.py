import cv2
import matplotlib.pyplot as plt
from helper import *


collectList1 = []
collectList2 = []
collectList3 = []


def ShapeDetection(img, imgContour):
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
        # tmp=map_g_to_temp(np.mean(imgContour[x:x+w, y:y+h]))
        # tmp = map_g_to_temp(np.max(imgContour))
        # collectList.append(tmp)

        ans1, ans2, ans3 = show_temperature_distribution(
            imgContour, x, y, w, h)
        collectList1.append(ans1)
        collectList2.append(ans2)
        collectList3.append(ans3)

        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(imgContour, objType, (x+(w//2), y+(h//2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        print(CornerNum, area)
    else:
        collectList1.append(0)
        collectList2.append(0)
        collectList3.append(0)


def process_img(srcPath, dstPath, fileName):
    img = cv2.imread(srcPath+fileName+'.pgm', 0)
    imgGray = img  # cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    imgContour = imgGray.copy()
    ret, imgBinary = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    conv_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img_dilate = cv2.dilate(imgBinary, conv_kernel)
    img_erod = cv2.erode(img_dilate, conv_kernel)

    imgCanny = cv2.Canny(img_erod, 60, 60)
    ShapeDetection(imgCanny, imgContour)

    cv2.imwrite(midPath+fileName+'_Gray.jpg', imgGray)
    cv2.imwrite(midPath+fileName+'_Binary.jpg', imgBinary)
    cv2.imwrite(midPath+fileName+'_Canny.jpg', imgCanny)
    cv2.imwrite(dstPath+fileName+'_Contour.jpg', imgContour)


path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
midPath = path+'/middleFile/'
dstPath = path+'/result/'
listName = './img_lists/vent.txt'

fp = open(listName, 'r')
filenames = [each.rstrip('\r\n') for each in fp.readlines()]
print(filenames)
for fileName in filenames:
    process_img(srcPath, dstPath, fileName)

print(collectList1)
print(collectList1)
print(collectList1)

fig = plt.figure(figsize=(4, 4), dpi=300)
x_lable = [int(each)/1000 for each in filenames]
plt.plot(x_lable, collectList1, marker='o', label="up")
plt.plot(x_lable, collectList2, marker='D', label="target")
plt.plot(x_lable, collectList3, marker='*', label="below")
plt.show()
