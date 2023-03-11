# 对近距离拍摄，未作分割的图像，已知破损数目的情况下，可精准定位——可以结合前面极大极小值的方法，确认数目后进行定位

from scipy import ndimage as ndi
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
import cv2


def draw_without_axis_many(cnt, imgs, strs):
    fig, axes = plt.subplots(1, 3, figsize=(8, 3), sharex=True, sharey=True,
                             subplot_kw={'adjustable': 'box'})
    for i in range(cnt):
        axes[i].imshow(imgs[i], cmap=plt.cm.gray)
        axes[i].axis('off')
        axes[i].set_title(strs[i])
    axes[2].plot(coordinates[:, 1], coordinates[:, 0], 'r.')
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    # im = cv2.imread('/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_pyg/421802_9_pyrDown_1_restore.bmp',0)
    # read_path = './mask/grabcut/'
    # num_list = ['421802_raw', '424654']

    read_path = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'
    num_list = [463202, 470328, 489938]
    for num in num_list:
        bmp_name = read_path+str(num)+".bmp"
        im = cv2.imread(bmp_name, 0)
        im = im[:, 0:50]
        image_max = ndi.maximum_filter(im, size=12, mode='constant')
        coordinates = peak_local_max(im, min_distance=5, num_peaks=4)

        imgs = [im, image_max, im]
        strs = ['Original', 'Maximum filter', 'Peak local max']
        draw_without_axis_many(3, imgs, strs)
