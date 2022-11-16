import cv2
import os
import numpy as np

suffixList=('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')

class helper():
    def __init__(self):
        self.tmp = 0
        
    def get_img_file(directionName):
        imagelist = []
        for parent, dirnames, filenames in os.walk(directionName):
            for filename in filenames:
                if filename.lower().endswith(suffixList):
                    imagelist.append(os.path.join(parent, filename))
            return imagelist


    def pic2bin(picName):
        a = cv2.imread(picName)
        ext = os.path.splitext(picName)
        a.tofile(ext[0]+".dat")
        print(a.shape)


    def bin2pic(picName):
        data = np.fromfile(picName, np.uint8).reshape(36, 35, 3)
        cv2.imwrite("test_bin2pic.png",data)
        cv2.imshow("test_bin2pic",data)
        cv2.waitKey(0)