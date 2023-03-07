import cv2
import os
import numpy as np


# # 对图像作反色，几乎完全无效
# def image_reverse(num, save_path, img):
#     cur_name = save_path+str(num)+"_reverse_"+str(cnt)+".png"
#     cv2.imwrite(cur_name, 255-img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
#     size = os.path.getsize(cur_name)
#     print("png_reverse: ", cnt, " ", size)
#     return cur_name


# # 对图像作除法，效果明显
# def image_div(num, save_path, img, divisor):
#     cur_name = save_path+str(num)+"_div"+str(divisor)+'_'+str(cnt)+".png"
#     cv2.imwrite(cur_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
#     size = os.path.getsize(cur_name)
#     print("png_div: ", cnt, " ", size)
#     return cur_name


# 对图像降低分辨率，直接取左上角，效果明显
def image_reduce_resolution(num, save_path, img, divisor):
    cur_name = save_path+str(num)+"_reduce"+str(divisor)+'_'+str(cnt)+".png"
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


# # 对图像降低分辨率，cv2.pyrDown，太影响破损检测
# def image_pyrDown(num, save_path, img, divisor):
#     cur_name = "{0}/{1}_{2}_reduce_{3}.png".format(
#         save_path, num, cnt, divisor)
#     for i in range(divisor-1):
#         img = cv2.pyrDown(img)
#     cv2.imwrite(cur_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
#     size = os.path.getsize(cur_name)
#     print("png_pyrDown: ", cnt, " ", size)
#     return cur_name


def test_para_for_png(num, save_path, img, cnt):
    prefix_name = "{0}/{1}_{2}".format(save_path, num, cnt)
    cur_name = "{0}.png".format(prefix_name)
    restore_name = "{0}_restore.bmp".format(prefix_name)

    cv2.imwrite(cur_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png: ", cnt, " ", size)

    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0))

    # cur_name = image_reverse(num, save_path, img)
    # cv2.imwrite(restore_name, 255-cv2.imread(cur_name, 0))

    # divisor = 32
    # cur_name = image_div(num, save_path, img, divisor)
    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0)*divisor)

    divisor = 2
    cur_name = image_reduce_resolution(num, save_path, img, divisor)
    cv2.imwrite(restore_name, cv2.imread(cur_name, 0))

    # divisor = 2
    # cur_name = image_pyrDown(num, save_path, img, divisor)
    # cv2.imwrite(restore_name, cv2.imread(cur_name, 0))

    size = os.path.getsize(restore_name)
    print("restore.bmp: ", size)


if __name__ == '__main__':
    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    save_path = './selected_pic_for_test_compression_png/output'

    num_list = [421802]
    for num in num_list:
        cur_name = read_path+str(num)+".bmp"
        img = cv2.imread(cur_name, 0)

        size = os.path.getsize(cur_name)
        print("bmp: ", size)

        for cnt in range(9, 10):
            test_para_for_png(num, save_path, img, cnt)
