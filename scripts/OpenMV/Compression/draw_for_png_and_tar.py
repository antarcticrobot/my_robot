# 对文件夹进行png和Linux压缩命令的压缩率计算

import os
from helpers import *


record = []
for i in range(4):
    record.append([])


def get_size_for_suffix(read_path_0, read_path_1, suffix, arr):
    arr.append(os.path.getsize(read_path_0+suffix))
    for num in range(10):
        arr.append(os.path.getsize(read_path_1+str(num)+suffix))


if __name__ == '__main__':
    read_path_0 = '/home/yr/热成像数据_存档_排烟管/for_compression/2023_02_20_1630_pyg_raw_bmp'
    read_path_1 = '/home/yr/热成像数据_存档_排烟管/for_compression/output/test_tar/'

    record[0].append(get_size_for_folder(read_path_0))
    root_path = '/home/yr/热成像数据_存档_排烟管/for_compression/output/'
    for num in range(10):
        record[0].append(get_size_for_folder(root_path+str(num)))

    suffixs = ['.tar.gz', '.tar.bz2', '.7z']
    for i in range(len(suffixs)):
        get_size_for_suffix(read_path_0, read_path_1, suffixs[i],  record[i+1])

    draw_Line_3(record, "原始图像与png压缩级别",
                ["Linux压缩前", "tar.gz", "tar.bz2", '7z'], [-0.4, -0.2, 0, 0])
