import cv2
import os


def test_para_for_png(img, path_name, cnt):
    cur_name = path_name+"_"+str(cnt)+".png"
    cv2.imwrite(cur_name, img, [cv2.IMWRITE_PNG_COMPRESSION, cnt])
    size = os.path.getsize(cur_name)
    print("png: ", cnt, " ", size)

    restore_name = path_name+"_"+str(cnt)+"_restore.bmp"
    cv2.imwrite(restore_name, cv2.imread(cur_name, 0))
    size = os.path.getsize(restore_name)
    print("restore.bmp: ", size)


if __name__ == '__main__':
    path_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/421802'
    save_name = './selected_pic_for_test_compression/output/421802'
    cur_name = path_name+".bmp"
    img = cv2.imread(cur_name, 0)

    size = os.path.getsize(cur_name)
    print("bmp: ", size)

    for cnt in range(10):
        test_para_for_png(img, save_name, cnt)
