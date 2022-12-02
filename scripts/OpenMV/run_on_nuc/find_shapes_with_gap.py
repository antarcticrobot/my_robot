import cv2
import matplotlib.pyplot as plt
from helper import *
# from find_shapes import *

path = '/home/yr/热成像数据_存档/2022_11_30_1100_tqyb0'
srcPath = path+'/raw/'
midPath = path+'/middleFile/'
dstPath = path+'/result/'
listName = path+'/img_lists/wall.txt'

fp = open(listName, 'r')
filenames = [each.rstrip('\r\n') for each in fp.readlines()]
collectList=[]
for fileName in filenames:
    img=cv2.imread(srcPath+fileName+'.pgm',0)
    collectList.append(map_g_to_temp(np.max(img)))
tmpList=[36.11764705882353, 35.84313725490196, 35.84313725490196, 35.568627450980394, 32.0, 29.529411764705884, 28.15686274509804, 27.607843137254903, 26.784313725490193, 26.784313725490193, 26.784313725490193, 26.235294117647058, 25.137254901960787, 24.313725490196077]
for num in tmpList:
    collectList.append(num)

x_lable = [int(each)/1000 for each in filenames]
tmpList=['119245', '162653', '235323', '267425', '305225', '317820', '327104', '333771', '352649', '359312', '365131', '372616', '388428', '401730']
tmpList=[(int(each)/1000  + 6000) for each in tmpList]
for num in tmpList:
    x_lable.append(num)

fig = plt.figure(figsize=(4, 4), dpi=300)
plt.plot(x_lable, collectList, marker='o', label="up")
plt.show()
