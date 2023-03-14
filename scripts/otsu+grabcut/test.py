import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches

image = cv2.imread('/home/yr/热成像数据_存档_排烟管/2023_02_20_1630_pyg/rainbow/421802.jpg')

cv2.namedWindow("result",cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
cv2.rectangle(image,(3,58),(12,78),(0,255,255),1)
cv2.rectangle(image,(12,59),(23,79),(0,255,255),1)
cv2.rectangle(image,(23,60),(32,80),(0,255,255),1)
cv2.imshow("result",image)
cv2.waitKey()