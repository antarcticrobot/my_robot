import cv2
import matplotlib.pyplot as plt
from helper import *


def cal_for_max_of_wall(path):
    srcPath = path+'/raw/'
    midPath = path+'/middleFile/'
    dstPath = path+'/result/'
    listName = path+'/img_lists/wall.txt'
    fp = open(listName, 'r')
    filenames = [each.rstrip('\r\n') for each in fp.readlines()]
    collectList = []
    for fileName in filenames:
        img = cv2.imread(srcPath+fileName+'.pgm', 0)
        collectList.append(map_g_to_temp(np.max(img)))
    return filenames, collectList


fig = plt.figure(figsize=(4, 4), dpi=300)

path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
filenames, collectList = cal_for_max_of_wall(path)
x_lable = [int(each)/1000 for each in filenames]
plt.plot(x_lable, collectList, marker='o')

path = '/home/yr/热成像数据_存档/2022_11_28_1400_tqyb17'
filenames, collectList = cal_for_max_of_wall(path)
x_lable = [int(each)/1000 for each in filenames]
plt.plot(x_lable, collectList, marker='D')

path = '/home/yr/热成像数据_存档/2022_11_30_1100_tqyb0'
filenames, collectList = cal_for_max_of_wall(path)
x_lable = [int(each)/1000 for each in filenames]
plt.plot(x_lable, collectList, marker='*')

plt.show()
