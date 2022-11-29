import cv2
import matplotlib.pyplot as plt
from helper import *

collectList = []


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
        tmp = map_g_to_temp(np.max(imgContour))
        collectList.append(tmp)

        show_temperature_distribution(imgContour, x, y, w, h)

        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(imgContour, objType, (x+(w//2), y+(h//2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        print(CornerNum, area)
    else:
        collectList.append(0)


def process_img(srcPath, dstPath, fileName):
    img = cv2.imread(srcPath+fileName+'.pgm')
    imgContour = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
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

print(collectList)

fig = plt.figure(figsize=(4, 4), dpi=300)
x_lable = [int(each)/1000 for each in filenames]
print(len(filenames))
print(len(x_lable))
print(len(collectList))
plt.plot(filenames, collectList)
plt.plot()
plt.show()
# fig.savefig("画布")
