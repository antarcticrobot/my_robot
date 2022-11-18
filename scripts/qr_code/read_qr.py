#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
读取二维码
'''
import cv2

# 读取二维码图片
img = cv2.imread("pic1.jpg")
# 初始化cv2的二维码检测器
detector = cv2.QRCodeDetector()
# 解码
data, bbox, straight_qrcode = detector.detectAndDecode(img)
# 如果解码成功
if bbox is not None:
    print(f"QRCode data:\n{data}")
    # 用线条显示图像
    # 边框长度
    n_lines = len(bbox)
    for i in range(n_lines):
        # 输出
        point1 = tuple(bbox[i][0])
        point2 = tuple(bbox[(i + 1) % n_lines][0])
        # cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)
# 显示结果
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
