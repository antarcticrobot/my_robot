# import imageio
import imageio.v2 as imageio

import os


def test_para_for_gif(img, path_name, cnt):
    cur_name = path_name+"_"+str(cnt)+".gif"
    imageio.imsave(cur_name,img)
    size = os.path.getsize(cur_name)
    print("gif: ", cnt, " ", size)

    restore_name = path_name+"_"+str(cnt)+"_restore.bmp"
    img2 = imageio.imread(cur_name, pilmode='L')	
    imageio.imsave(restore_name,img2)
    size = os.path.getsize(restore_name)
    print("restore.bmp: ", size)


if __name__ == '__main__':
    num = 417997
    # num = 421802
    # num = 426080
    path_name = '/home/yr/热成像数据_存档_排烟管/外裹纸/2023_02_20_1630_pyg/raw/'+str(num)
    save_name = './selected_pic_for_test_compression_gif/output/'+str(num)
    cur_name = path_name+".bmp"
    img = imageio.imread(cur_name, pilmode='L')	

    size = os.path.getsize(cur_name)
    print("bmp: ", size)

    for cnt in range(1):
        test_para_for_gif(img, save_name, cnt)
