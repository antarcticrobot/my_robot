import cv2
import matplotlib.pyplot as plt

path = '/home/yr/热成像数据_存档/2022_11_28_1100_tqyb17'
srcPath = path+'/raw/'
fileName = '1325532'

img = cv2.imread(srcPath+fileName+'.pgm', 0)
img2 = cv2.imread(srcPath+fileName+'.pgm', 0)
cv2.line(img2, (0, 40), (160, 40), (255, 0, 0))
cv2.line(img2, (72, 0), (72, 120), (255, 0, 0))
cv2.imwrite('./withline.jpg', img2)

fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(range(160), img[40:41, :].flatten(), marker='o', label="collectList1")
ax2 = fig.add_subplot(212)
ax2.plot(range(120), img[:, 56:57].flatten(), marker='o', label="collectList1")
plt.plot()
plt.show()
