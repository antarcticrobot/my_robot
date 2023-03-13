import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


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
        str = '%s' % (height)
        plt.text(rect.get_x()+rect.get_width() + offset, 1.01*height, str)


def print_ratio(rects, offset):
    for rect in rects:
        height = rect.get_height()
        str = '%.3f' % (height)
        plt.text(rect.get_x()+rect.get_width() + offset, 1.01*height, str)


def print_percentage(rects, offset):
    for rect in rects:
        height = rect.get_height()
        str = '%.2f%%' % (height*100)
        plt.text(rect.get_x()+rect.get_width() + offset, 1.01*height, str)


# # 对图像作反色，几乎完全无效
# # 对图像作除法，效果明显
def image_div(img,  prefix, cnt, divisor, record, jump_restrore=False):
    result_name, restore_name = get_two_names(prefix, "div", divisor)
    cv2.imwrite(result_name, img/divisor, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record.append(print_size("div result: ", result_name))
    if (jump_restrore == False):
        do_restrore(result_name, restore_name, divisor)


# 对图像降低分辨率，直接取左上角，效果明显
def image_shrink(img,  prefix, cnt, divisor, record, jump_restrore=False):
    result_name, restore_name = get_two_names(prefix, "shrink", divisor)
    row = int(120/divisor)
    col = int(160/divisor)
    tmp = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            tmp[i, j] = (img[i*divisor, j*divisor]).astype(np.uint8)
    cv2.imwrite(result_name, tmp, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    record.append(print_size("shrink result: ", result_name))
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


def to_percent(temp, position):
    return '%1.1f' % (100*temp)


def drawHistogram_3(lists, xlabel, strs=["raw", "div", "shrink"], offsets=[-0.05, -0.03, -0.05], window_x=8, window_y=6):
    prepare_window(window_x, window_y)
    total_width, n = 0.5, len(lists)   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    my_fontsize = 16

    x = np.arange(len(lists[0]))   # 横坐标范围
    for i in range(n):
        # lists[i] = np.array(lists[i]).flatten()
        lists[i] = np.array(lists[i]).mean(axis=1)
        # lists[i] = np.array(lists[i]).std(axis=0)
        lists[i] = [x/20278 for x in lists[i]]

    plt.figure()
    plt.title("")
    plt.xlabel(xlabel, fontsize=my_fontsize)
    # x_ticks=["raw"]
    x_ticks = []
    # for num in range(10-len(lists[0]), 10):
    for num in range(1, len(lists[0])+1):
        x_ticks.append(str(num))
    plt.xticks(x, np.array(x_ticks))

    # plt.ylabel("结果图片大小/Byte", fontsize=my_fontsize)
    # print_value(rect[1], - 0.4)
    # plt.ylabel("压缩比", fontsize=my_fontsize)
    # print_ratio(rect[1],- 0.4)
    # plt.ylabel("压缩率/%", fontsize=my_fontsize)
    plt.ylabel("压缩率均值/%", fontsize=my_fontsize)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    plt.ylim((0, 0.5))

    # plt.ylabel("压缩率标准差/%", fontsize=my_fontsize)
    # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    # plt.ylim((0,0.025))

    for i in range(n):
        rect = (plt.bar(x + (-n/2+i)*width,
                lists[i], width=width, label=strs[i]))
        print_percentage(rect, offsets[i])

    plt.legend()
    plt.show()


def draw_Line_3(lists, xlabel, strs=["raw", "div", "shrink"], offsets=[-0.05, -0.03, -0.05], window_x=8, window_y=6):
    prepare_window(window_x, window_y)
    total_width, n = 0.5, len(lists)   # 柱状图总宽度，有几组数据
    width = total_width / n   # 单个柱状图的宽度
    my_fontsize = 16

    for i in range(n):
        lists[i] = [cur/(20278*789) for cur in lists[i]]

    plt.figure()
    plt.title("")
    plt.xlabel(xlabel, fontsize=my_fontsize)
    x_ticks = ["raw"]
    for num in range(0, len(lists[0])+1):
        x_ticks.append(str(num))
    x = np.arange(len(lists[1]))   # 横坐标范围
    plt.xticks(x, x_ticks)

    plt.ylabel("压缩率/%", fontsize=my_fontsize)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))
    # plt.ylim((0.2, 0.5))

    for i in range(n):
        rect = (plt.bar(x + (-n/2+i)*width,
                lists[i], width=width, label=strs[i]))
        # print_percentage(rect, offsets[i])

    plt.legend()
    plt.show()


def get_img_num(directionName):
    num_list = []
    for parent, dirnames, filenames in os.walk(directionName):
        for filename in filenames:
            if filename.lower().endswith('.bmp'):
                fname1, fname2 = os.path.split(filename)
                num_list.append(str.split(fname2, '.bmp')[0])
    return num_list


def prepare_window(window_x, window_y):
    plt.rcParams["font.sans-serif"] = ['SimHei']  # 设置字体
    plt.rcParams["axes.unicode_minus"] = False  # 正常显示负号
    plt.rcParams['figure.figsize'] = (window_x, window_y)


def get_size_for_folder(pathvar):
    lst = os.listdir(pathvar)
    size = 0
    for i in lst:
        pathnew = os.path.join(pathvar, i)
        if os.path.isfile(pathnew):
            size += os.path.getsize(pathnew)
        elif os.path.isdir(pathnew):
            size += get_size_for_folder(pathnew)
    return size
