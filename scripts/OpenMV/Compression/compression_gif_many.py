# import imageio
import imageio.v2 as imageio

def compose_gif():
    # img_paths = ["417997_0.gif", "421802_0.gif", "426080_0.gif"]
    img_paths = ["417997.bmp", "421802.bmp", "426080.bmp"]
    gif_images = []
    for path in img_paths:
        # gif_images.append(imageio.imread('/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_compression_gif/output/'+path))
        gif_images.append(imageio.imread('/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_compression_gif/'+path))
        print(path)
    imageio.mimsave("/home/yr/catkin_ws/src/my_robot/selected_pic_for_test_compression_gif/output/test_direct.gif", gif_images, fps=1)

compose_gif()