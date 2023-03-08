import cv2
import os
import math
import numpy as np


def print_size(str, file_path):
    print(str, os.path.getsize(file_path))


def do_restrore(result_name, restore_name):
    cv2.imwrite(restore_name, cv2.imread(result_name, 0))
    print_size("restore: ", restore_name)


def get_two_names(prefix, fuc, divisor):
    result_name = "{0}_{1}_{2}.png".format(prefix, fuc, divisor)
    restore_name = "{0}_{1}_{2}_restore.bmp".format(prefix, fuc, divisor)
    return result_name, restore_name


# # 对图像作反色，几乎完全无效
# # 对图像作除法，效果明显
def image_div(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "div", divisor)
    cv2.imwrite(result_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    print_size("div result: ", result_name)
    do_restrore(result_name, restore_name)


# 对图像降低分辨率，cv2.pyrDown，太影响破损检测
def image_pyrDown(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "pyrDown", divisor)

    tmp = img
    for i in range(divisor-1):
        tmp = cv2.pyrDown(tmp)

    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    print_size("pyrDown result: ", result_name)
    do_restrore(result_name, restore_name)


# 对图像降低分辨率，直接取左上角，效果明显
def image_reduce_resolution(img,  prefix, divisor):
    result_name, restore_name = get_two_names(prefix, "reduce", divisor)

    row = int(120/divisor)
    col = int(160/divisor)
    tmp = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            tmp[i, j] = (img[i*divisor, j*divisor]).astype(np.uint8)

    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    print_size("reduce result: ", result_name)
    do_restrore(result_name, restore_name)


def test_para_for_png(img, num, save_path, cnt):
    prefix = "{0}/{1}_{2}".format(save_path, num, cnt)
    png_name = "{0}.png".format(prefix)

    cv2.imwrite(png_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(png_name)
    print("png: ", cnt, " ", size)

    for divisor in range(1, 4):
        image_div(img, prefix, int(math.pow(2, divisor)))
        image_pyrDown(img,  prefix, divisor)
        image_reduce_resolution(img,  prefix, divisor)


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    num_list = [421802]
    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        print_size("bmp: ", bmp_name)

        img = cv2.imread(bmp_name, 0)
        for cnt in range(9, 10):
            test_para_for_png(img, num, save_path, cnt)
