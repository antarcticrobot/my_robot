# 对一张侧墙的图片，绘制直方图想对其包络线进行拟合——失败，不是什么特别的曲线

import cv2
import numpy as np
import matplotlib.pyplot as plt


# 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
def draw_hist(myList, Title, Xlabel, Ylabel):
    m = plt.hist(myList,256)
    plt.xlabel(Xlabel)
    plt.ylabel(Ylabel)
    plt.title(Title)
    return m


path = '/home/yr/热成像数据_存档/通风口无物品/2022_11_30_1400_tqyb0'
srcPath = path+'/raw/'
# fileName = '1348297'
# fileName = '1385475'
# fileName = '1363976'
fileName = '792471'

img = cv2.imread(srcPath+fileName+'.pgm', 0)

mean=np.array(img).mean()
std=np.array(img).std()
print('x的均值',mean)
print('x的方差',std)
z = draw_hist(img.flatten(), 'AreasList', 'Area', 'number')
plt.show()

# plt.plot()
# plt.show()
# import matplotlib.pyplot as plt
# import matplotlib.mlab as mlab
# import numpy as np
# from scipy.optimize import curve_fit
# from scipy import asarray as ar,exp
# import numpy as np

# # 参数依次为list,抬头,X轴标签,Y轴标签,XY轴的范围
# def draw_hist(myList,Title,Xlabel,Ylabel,Xmin,Xmax,Ymin,Ymax):
#      m=plt.hist(myList,100)
#      plt.xlabel(Xlabel)
#      plt.xlim(Xmin,Xmax)
#      plt.ylabel(Ylabel)
#      plt.ylim(Ymin,Ymax)
#      plt.title(Title)
# # plt.show()
# # fig=plt.figure()
# # plt.show()
#      return m

# #读取数据
# feedlist= open('./test.csv')
# x=[]
# for feedurl in feedlist:
#     feedurl = feedurl.strip('\n')
#     feedurl=float(feedurl)
#     x.append(feedurl)
# print(x)
# #根据数据生成直方图
# mean=np.array(x).mean()
# std=np.array(x).std()
# print('x的均值',mean)
# print('x的方差',std)
# print('置信区间',mean-2*std,mean+2*std)
# z=draw_hist(x,'AreasList','Area','number',0,10000,0,350)
# x=z[1][0:len(z[1])-1]
# y=z[0]
# plt.plot(x,y,color='b')
# plt.xlim(0,10000)
# plt.ylim(0,350)
# plt.axis('on')
# x1=[mean+2*std]*100
# x1=np.array(x1)
# y1=np.linspace(1,350,100)
# plt.plot(x1,y1,color='r')
# print(x1)
# plt.show()
