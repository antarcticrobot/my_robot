import numpy as np
import cv2
import matplotlib.pyplot as plt
from helper import *


def get_pyg(src_name, mask_name, save_name, result_name):
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
    # cv2.imwrite(save_name, imgGrabCut)

    plt.figure(figsize=(8, 2.5))
    plt.subplot(131), plt.axis('off'), plt.title("恢复图像")
    plt.imshow(image, 'gray')
    plt.subplot(132), plt.axis('off'), plt.title("分割结果")
    plt.imshow(imgGrabCut, 'gray')

    plt.subplot(133), plt.yticks(np.arange(0, 255, step=10)), plt.title("破损检测")


    list1=get_maxs(image)
    list1 = np.array(list1)
    plt.plot(list1)
    extrema_1 = signal.argrelextrema(list1, np.greater, order=1)
    extrema_2 = signal.argrelextrema(list1, np.less, order=1)

    # plt.tight_layout()
    plt.savefig(result_name)
    # plt.show()


if __name__ == '__main__':
    # src_name = '/home/yr/热成像数据_存档/2023_01_03_2110_tqyb4/rainbow/1884624.jpg'
    # mask_name = "./mask/1884624.jpg"
    # src_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/421802.bmp'
    # mask_name = "./mask/421802.bmp"

    read_path = '/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/'
    mask_path = "./mask/"
    result_path = '/home/yr/2023_0413/'
    num_list = ['421802_9_div_2_restore', '421802_9_div_4_restore',
                '421802_9_div_8_restore', '421802_9_div_16_restore']
    num_list = ['421802_9_reduce_2_restore', '421802_9_reduce_3_restore',
                '421802_9_reduce_4_restore']
    for num in num_list:
        src_name = read_path+str(num)+".bmp"
        mask_name = mask_path+str(num)+".bmp"
        save_name = result_path+str(num)+".bmp"
        result_name = result_path+str(num)+"_cut.png"

        get_pyg(src_name, mask_name, save_name, result_name)
