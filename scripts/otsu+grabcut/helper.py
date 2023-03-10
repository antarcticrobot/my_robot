import os
import cv2 as cv


def get_img_num(directionName):
    num_list = []
    for parent, dirnames, filenames in os.walk(directionName):
        for filename in filenames:
            if filename.lower().endswith('.bmp'):
                fname1, fname2 = os.path.split(filename)
                num_list.append(str.split(fname2, '.bmp')[0])
    return num_list
