import cv2
from helper import *


def print_temperature_of_selected_spots(fileName):
    img_gray = cv2.imread(fileName, 0)
    print("fileName: ", fileName)
    for i in range(0, 10):
        print(str(img_gray[i][i*10])+" "+str(map_g_to_temp(img_gray[i][i*10])))


def print_temperature_of_selected_spots(fileName1, fileName2, fileName3, fileName4):
    img_gray_1 = cv2.imread(fileName1, 0)
    img_gray_2 = cv2.imread(fileName2, 0)
    img_gray_3 = cv2.imread(fileName3, 0)
    img_gray_4 = cv2.imread(fileName4, 0)
    for i in range(0, 10):
        print(str(img_gray_1[i][i*10])+" "+str(img_gray_2[i][i*10]) +
              " "+str(img_gray_3[i][i*10])+" "+str(img_gray_4[i][i*10]))


# print_temperature_of_selected_spots("1.bmp")
# print_temperature_of_selected_spots("2.pgm")
# print_temperature_of_selected_spots("3.jpg")
# print_temperature_of_selected_spots("4.jpeg")

print_temperature_of_selected_spots("1.bmp", "2.pgm", "3.jpg", "4.jpeg")
