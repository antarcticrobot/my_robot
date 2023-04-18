import numpy as np
import cv2
import matplotlib.pyplot as plt
from helper import *
from matplotlib.gridspec import GridSpec


def get_pyg(src_name, mask_name, save_name, result_name, ax, picNum=1):
    image = cv2.imread(src_name)
    maskImg = cv2.imread(mask_name, flags=0)  # 读取掩模图像(xupt)

    maskImg = 255-maskImg
    mask = np.zeros(image.shape[:2], dtype="uint8")
    mask[maskImg > 0] = cv2.GC_PR_FGD
    mask[maskImg == 0] = cv2.GC_BGD
    fgModel = np.zeros((1, 65), dtype="float")  # 前景模型, 13*5
    bgModel = np.zeros((1, 65), dtype="float")  # 背景模型, 13*5
    iter = 5
    (mask, bgModel, fgModel) = cv2.grabCut(image, mask, None, bgModel, fgModel, iter,
                                           mode=cv2.GC_INIT_WITH_MASK)  # 基于掩模图像初始化

    # 将所有确定背景和可能背景像素设置为 0，而确定前景和可能前景像素设置为 1
    maskOutput = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD), 0, 1)
    maskGrabCut = 255 - (maskOutput * 255).astype("uint8")
    imgGrabCut = cv2.bitwise_and(image, image, mask=maskGrabCut)

    # ylable_without_ticks(ax[picNum, 0], "温度精度降低"+str(pow(2,cnt+1))+"倍")
    ylable_without_ticks(ax[picNum, 0], "分辨率降低"+str(cnt+2)+"倍")

    ax[0, 0].set_title("恢复图像")
    ax[picNum, 0].imshow(image, 'gray')

    ax[picNum, 1].set_xticks([]), ax[picNum, 1].set_yticks([])
    ax[0, 1].set_title("分割结果")
    ax[picNum, 1].imshow(imgGrabCut, 'gray')

    maxs=get_maxs(image)
    ax[picNum, 2].set_xlim([0,len(maxs)]), ax[picNum, 2].set_ylim([120,220])
    ax[picNum, 2].set_xticks(range(0,len(maxs)+1,10))
    ax[picNum, 2].set_yticks(range(120,221,20))
    ax[picNum, 2].set_ylabel('最高温度点的灰度值'),    ax[picNum, 2].set_xlabel('垂直切片位置')
    ax[0, 2].set_title("破损检测")
    ax[picNum, 2].plot(np.array(maxs))


if __name__ == '__main__':
    # src_name = '/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/rainbow/1884624.jpg'
    # mask_name = "./mask/1884624.jpg"
    # src_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/421802.bmp'
    # mask_name = "./mask/421802.bmp"

    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    mask_path = "./mask/"
    result_path = '/home/yr/2023_0413/'
    # num_list = ['421802_9_div_2_restore', '421802_9_div_4_restore',
    #             '421802_9_div_8_restore', '421802_9_div_16_restore']
    num_list = ['421802_9_reduce_2_restore', '421802_9_reduce_3_restore',
                '421802_9_reduce_4_restore']

    fig = plt.figure(dpi=100,figsize=[6.5,6], constrained_layout=True)
    # fig = plt.figure(dpi=100,figsize=[5.5,6], constrained_layout=True)
    ax = fig.subplots(len(num_list), 3)
    cnt = 0
    for num in num_list:
        src_name = read_path+str(num)+".bmp"
        mask_name = mask_path+str(num)+".bmp"
        save_name = result_path+str(num)+".bmp"
        result_name = result_path+str(num)+"_cut.png"

        get_pyg(src_name, mask_name, save_name, result_name, ax, cnt)
        cnt += 1

    # fig.tight_layout()
    fig.show()
    fig.waitforbuttonpress()
    # fig.savefig(result_path+'div.png')
