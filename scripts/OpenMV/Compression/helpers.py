import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def get_two_names(prefix, fuc, divisor):
    result_name = "{0}_{1}_{2}.png".format(prefix, fuc, divisor)
    restore_name = "{0}_{1}_{2}_restore.bmp".format(prefix, fuc, divisor)
    return result_name, restore_name


def print_size(str, file_path):
    size = os.path.getsize(file_path)
    # print(str, size)
    return size


def do_restrore(result_name, restore_name, multi_para=1):
    cv2.imwrite(restore_name, cv2.imread(result_name, 0)*multi_para)
    print_size("restore: ", restore_name)


def print_value(rects, offset):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/3. +
                 offset, 1.01*height, '%s' % (height))


# # 对图像作反色，几乎完全无效
# # 对图像作除法，效果明显
def image_div(img,  prefix, cnt, divisor, record, jump_restrore=False):
    result_name, restore_name = get_two_names(prefix, "div", divisor)
    cv2.imwrite(result_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record.append(print_size("div result: ", result_name))
    if (jump_restrore == False):
        do_restrore(result_name, restore_name, divisor)


# 对图像降低分辨率，直接取左上角，效果明显
def image_reduce_resolution(img,  prefix, cnt, divisor, record, jump_restrore=False):
    result_name, restore_name = get_two_names(prefix, "reduce", divisor)
    row = int(120/divisor)
    col = int(160/divisor)
    tmp = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            tmp[i, j] = (img[i*divisor, j*divisor]).astype(np.uint8)
    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record.append(print_size("reduce result: ", result_name))
    if (jump_restrore == False):
        do_restrore(result_name, restore_name)


# 对图像降低分辨率，cv2.pyrDown，太影响破损检测
def image_pyrDown(img,  prefix, cnt, divisor, jump_restrore=False):
    result_name, restore_name = get_two_names(prefix, "pyrDown", divisor)
    tmp = img
    for i in range(divisor-1):
        tmp = cv2.pyrDown(tmp)
    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    print_size("pyrDown result: ", result_name)
    if (jump_restrore == False):
        do_restrore(result_name, restore_name)


def drawHistogram_3(list1, list2, list3, str1="raw", str2="div", str3="reduce", offset1=-0.05, offset2=-0.03, offset3=-0.05):
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    total_width, n = 0.5, 3   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    my_fontsize = 16
    x = np.arange(len(list2))   # 横坐标范围

    plt.figure()
    plt.title("")
    plt.xlabel("png压缩级别", fontsize=my_fontsize)
    plt.xticks(x, range(10-len(list1), 10))
    plt.ylabel("结果图片大小/Byte", fontsize=my_fontsize)
    rect0 = plt.bar(x - width, list1, width=width, label=str1)
    rect1 = plt.bar(x, list2, width=width, label=str2)
    rect2 = plt.bar(x + width, list3, width=width, label=str3)
    print_value(rect0, offset1)
    print_value(rect1, offset2)
    print_value(rect2, offset3)
    plt.legend()
    plt.show()
