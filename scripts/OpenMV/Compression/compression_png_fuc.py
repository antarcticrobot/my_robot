import cv2
import os
import numpy as np


# 对图像作反色，几乎完全无效
def image_reverse(path_name, img):
    cur_name = path_name+"_reverse_"+str(cnt)+".png"
    cv2.imwrite(cur_name, 255-img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png_reverse: ", cnt, " ", size)
    return cur_name


# 对图像作除法，效果明显
def image_div(path_name, img, divisor):
    cur_name = path_name+"_div"+str(divisor)+'_'+str(cnt)+".png"
    cv2.imwrite(cur_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png_div: ", cnt, " ", size)
    return cur_name


# 对图像降低分辨率，效果明显
def image_reduce_resolution(path_name, img, divisor):
    cur_name = path_name+"_reduce"+str(divisor)+'_'+str(cnt)+".png"

    row = int(120/divisor)
    col = int(160/divisor)
    tmp = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            tmp[i, j] = (img[i*divisor, j*divisor]).astype(np.uint8)

    cv2.imwrite(cur_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png_reduce: ", cnt, " ", size)
    return cur_name


def test_para_for_png(img, path_name, cnt):
    cur_name = path_name+"_"+str(cnt)+".png"
    restore_name = path_name+"_"+str(cnt)+"_restore.bmp"

    cv2.imwrite(cur_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png: ", cnt, " ", size)

    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0))

    # cur_name = image_reverse(path_name, img)
    # cv2.imwrite(restore_name, 255-cv2.imread(cur_name, 0))

    # divisor = 16
    # cur_name = image_div(path_name, img, divisor)
    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0)*divisor)

    divisor = 1
    cur_name = image_reduce_resolution(path_name, img, divisor)
    cv2.imwrite(restore_name, cv2.imread(cur_name, 0))

    size = os.path.getsize(restore_name)
    print("restore.bmp: ", size)


if __name__ == '__main__':
    path_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/421802'
    save_name = './selected_pic_for_test_compression_png/output/421802'
    cur_name = path_name+".bmp"
    img = cv2.imread(cur_name, 0)

    size = os.path.getsize(cur_name)
    print("bmp: ", size)

    for cnt in range(0, 10):
        test_para_for_png(img, save_name, cnt)
