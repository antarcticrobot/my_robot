#!/usr/bin/env python
# -*- coding:utf-8 -*-

import cv2


def read_qr_code(img):
    detector = cv2.QRCodeDetector()
    data = detector.detectAndDecodeMulti(img)
    if data[0]:        
        # print(f"QRCode data:\n{data}")
        # print(f"bbox:\n{bbox}")
        # print(f"straight_qrcode.shape:\n{straight_qrcode.shape}")
        n_codes = len(data[1])
        for num in range(n_codes):
            print(f"QRCode data:\n{data[1][num]}")
            print(f"QRCode data:\n{data[2][num]}")
            n_lines = len(data[2][num])
            for i in range(n_lines):
                point1 = data[2][num][i]
                point1 = int(point1[0]), int(point1[1])
                point2 = data[2][num][(i + 1) % n_lines]
                point2 = int(point2[0]), int(point2[1])
                cv2.line(img, point1, point2, color=(0, 255, 0), thickness=2)

        cv2.imwrite("result.jpg", img)
        # cv2.imwrite("straight_qrcode.jpg", straight_qrcode)
        cv2.namedWindow("result", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.imshow("result", img)
        cv2.waitKey(0)


if __name__ == "__main__":
    img = cv2.imread("/home/yr/catkin_ws/src/my_robot/scripts/qr_code/images/pic1.jpg")
    # cv2.namedWindow("result", cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    # cv2.imshow("result", img)
    # cv2.waitKey(0)
    read_qr_code(img)
