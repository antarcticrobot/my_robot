from PIL import Image

root_name = '/home/yr/catkin_ws/src/my_robot'


def check():
    # # check png
    # path_name_1 = root_name+'/selected_pic_for_test_compression_png/421802.bmp'
    # # path_name_2 = root_name + \
    # #     '/selected_pic_for_test_compression_png/output/421802_0.png'
    # path_name_2 = root_name + \
    #     '/selected_pic_for_test_compression_png/output/421802_2_restore.bmp'

    # check gif
    path_name_1 = root_name+'/selected_pic_for_test_compression_gif/417997.bmp'
    # path_name_2 = root_name + \
    #     '/selected_pic_for_test_compression_gif/output/421802_0.gif'
    path_name_2 = root_name + \
        '/selected_pic_for_test_compression_gif/output/417997_0_restore.bmp'

    img1 = Image.open(path_name_1)
    img2 = Image.open(path_name_2)

    # print((img2), " ", (img1))

    cnt = 0
    for i in range(160):
        for j in range(120):
            if (img2.getpixel((i, j)) != img1.getpixel((i, j))):
                # print(i, " ", j)
                # print(type(img2.getpixel((i, j))), " ", type(img1.getpixel((i, j))))
                print(img2.getpixel((i, j)), " ", img1.getpixel((i, j)))
                cnt += 1
    print(cnt)


check()
