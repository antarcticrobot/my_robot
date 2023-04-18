import cv2
import matplotlib.pyplot as plt
from helper import *
from process_list_2 import cal_for_fuc_of_wall


def get_x_y_with_gap():
    path = '/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1100_tqyb0'
    srcPath, midPath, dstPath = get_full_paths(path)
    listName = path+'/img_lists/wall.txt'

    fp = open(listName, 'r')
    filenames = [each.rstrip('\r\n') for each in fp.readlines()]
    collectList = []
    for fileName in filenames:
        img = cv2.imread(srcPath+fileName+'.pgm', 0)
        collectList.append(map_g_to_temp(np.max(img)))
    tmpList1, tmpList2 = cal_for_fuc_of_wall(
        '/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1100_2_tqyb0', np.max)
    tmpList2[17] += 2
    collectList.extend(tmpList2)
    # print(tmpList2)
    x_lable = [int(each)/1000 for each in filenames]    
    tmpList1 = [(int(each) + 5050) for each in tmpList1]
    x_lable.extend(tmpList1)

    # fig = plt.figure(figsize=(4, 4), dpi=300)
    # plt.plot(x_lable, collectList, marker='o', label="up")
    # plt.show()
    x_lable = [each-x_lable[0]+100 for each in x_lable]
    return x_lable, collectList
