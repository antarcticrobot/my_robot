import os
import sys
import cv2

from queue import *

def imgstitcher(imgs):  # 传入图像数据 列表[] 实现图像拼接
    print("imgs.length",len(imgs))
    stitcher = cv2.Stitcher.create(cv2.Stitcher_PANORAMA)
    _result, pano = stitcher.stitch(imgs)
    print("_result",_result)
    if(_result==0):
        output = 'result' + '.png'
        cv2.imwrite(output, pano)
        print("拼接成功. %s 已保存!" % output)
    else:
        print("[INFO] image stitching failed ({})".format(status))


if __name__ == "__main__":
    # imgPath为图片所在的文件夹相对路径
    imgPath = '/home/yr/current_test/desk_rotate'

    imgList = os.listdir(imgPath)
    imgs = []
    for imgName in imgList:
        pathImg = os.path.join(imgPath, imgName)
        img = cv2.imread(pathImg)
        if img is None:
            print("图片不能读取：" + imgName)
            sys.exit(-1)
        imgs.append(img)
    imgstitcher(imgs)    # 拼接
