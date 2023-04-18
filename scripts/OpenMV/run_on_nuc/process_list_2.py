# 对多个时间序列的墙面数据，寻找最高温度或其他数字代表一张图

import cv2
import matplotlib.pyplot as plt
from helper import *


def cal_for_fuc_of_wall(path, fuc):
    srcPath, midPath, dstPath = get_full_paths(path)
    listName = path+'/img_lists/wall.txt'
    fp = open(listName, 'r')
    filenames = [each.rstrip('\r\n') for each in fp.readlines()]
    filenames=[int(each) for each in filenames]
    filenames.sort()
    collectList = []
    for fileName in filenames:
        img = cv2.imread(srcPath+str(fileName)+'.pgm', 0)
        img = cv2.blur(img, (3, 3))
        collectList.append(map_g_to_temp(fuc(img)))
    minX=int(filenames[0])    
    x_lable=[(int(each)-minX)/1000+100 for each in filenames] 
    # x_lable=[(int(each))/1000 for each in filenames]

    return x_lable, collectList


def plot_for_max_of_wall(path, ax1):
    x_lable, collectList=cal_for_fuc_of_wall(path, np.max)
    ax1.plot(x_lable, collectList, marker='o', markersize=2, linewidth=1)


if __name__ == "__main__":
    paths=[]
    paths.append('/home/yr/热成像数据_存档/通风口无物品/2022_11_28_1100_tqyb17')
    paths.append('/home/yr/热成像数据_存档/通风口无物品/2022_11_28_1400_tqyb17')
    paths.append('/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1100_tqyb0')
    paths.append('/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1400_tqyb0')
    paths.append('/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1100_2_tqyb0')

    fig=plt.figure(figsize=(4, 4), dpi=300)
    ax1=fig.add_subplot(111)
    for path in paths:
        plot_for_max_of_wall(path, ax1)
    plt.show()
