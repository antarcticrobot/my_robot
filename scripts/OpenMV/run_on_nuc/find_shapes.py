import cv2
from helper import *


def ShapeDetection(img, imgContour):
    contours, hierarchy = cv2.findContours(
        img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for obj in contours:
        area = cv2.contourArea(obj)
        perimeter = cv2.arcLength(obj, True)
        approx = cv2.approxPolyDP(obj, 0.02*perimeter, True)
        CornerNum = len(approx)
        x, y, w, h = cv2.boundingRect(approx)
        objType = get_shape_name(CornerNum, w, h)

        show_temperature_distribution(imgContour, x, y, w, h)

        cv2.rectangle(imgContour, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cv2.putText(imgContour, objType, (x+(w//2), y+(h//2)),
                    cv2.FONT_HERSHEY_COMPLEX, 0.4, (0, 0, 0), 1)
        print(x, y, w, h)
        print(CornerNum, objType, area)


def process_img(srcPath, dstPath, fileName):
    img = cv2.imread(srcPath+fileName+'.pgm')
    imgContour = img.copy()

    imgGray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    ret, imgBinary = cv2.threshold(
        imgGray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)
    imgBlur = cv2.GaussianBlur(imgBinary, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, 60, 60)
    ShapeDetection(imgCanny, imgContour)

    cv2.imwrite(dstPath+fileName+'_Gray.jpg', imgGray)
    cv2.imwrite(dstPath+fileName+'_Blur.jpg', imgBlur)
    cv2.imwrite(dstPath+fileName+'_Canny.jpg', imgContour)
    cv2.imwrite(dstPath+fileName+'_Contour.jpg', imgCanny)

    # cv2.imshow("Original img", img)
    # cv2.imshow("imgGray", imgGray)
    # cv2.imshow("imgBlur", imgBlur)
    # cv2.imshow("imgCanny", imgCanny)
    # cv2.imshow("shape Detection", imgContour)

    # cv2.waitKey()


path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
dstPath = path+'/result/'
listName = './img_lists/vent.txt'

fp = open(listName, 'r')
filenames = [each.rstrip('\r\n') for each in fp.readlines()]
print(filenames)
for fileName in filenames:
    process_img(srcPath, dstPath, fileName)
