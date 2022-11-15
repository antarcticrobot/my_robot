

from math import nan
import scipy
from scipy import io
import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata
import cv2
import matplotlib.pyplot as plt

# # def fun(x,y):
# #     return x**2+y**2

# # xy = np.random.rand(10,2)*5
# # z = fun(xy[:,0],xy[:,1])


# # znew = griddata(xy,z,(grid_x,grid_y))
# # print(znew)
# # print(znew.shape)


# # # python如何画三维图
# # import mpl_toolkits.mplot3d
# # ax = plt.subplot(111,projection = '3d')
# # ax.plot_surface(xnew,ynew,znew)
# # plt.show()

# path_infrared = '/home/yr/catkin_ws/src/my_robot/matlab/Image-registration/CAO-C2F/Example_Images/I13.jpg'
# path_visible = '/home/yr/catkin_ws/src/my_robot/matlab/Image-registration/CAO-C2F/Example_Images/V13.jpg'
# I1 = cv2.imread(path_infrared, 0)
# I2 = cv2.imread(path_visible, 0)
# extend = max(I1.shape)


# M = np.array([[0.459843740477301,	-0.00971970394861337,	-4.09401422931936e-05],
#               [0.0498730194649677,	0.523588343950058,	0.000158393188726247],
#               [169.137019015027,	-40.5830348423779,	1]])
# '''破案了 Matlab的.T不是转置的意思，而是取出T属性'''


# Imosaic = np.zeros((2*extend+I2.shape[0], 2*extend+I2.shape[1]))
# v, u = np.mgrid[0:Imosaic.shape[0], 0:Imosaic.shape[1]]
# u, v = u.flatten('F'), v.flatten('F')  # 这里原来没'F'，我说结果为啥不对呢
# u -= extend  # (4989696,)
# v -= extend
# # np.savetxt('D:/u.txt',u,fmt='%d')
# # np.savetxt('D:/v.txt',v,fmt='%d')

# utvt = np.hstack(
#     (np.reshape(u, (-1, 1)), np.reshape(v, (-1, 1)), np.ones((len(u), 1))))
# '''经验证，utvt和MATLAB一致'''


# utvt = np.dot(utvt, np.linalg.inv(M))
# ut = utvt[:, 0]/utvt[:, 2]
# vt = utvt[:, 1]/utvt[:, 2]
# # np.savetxt('D:/ut.txt',ut,fmt='%.4f')
# # np.savetxt('D:/vt.txt',vt,fmt='%.4f')


# # Matlab重排时，列优先
# # python重排时，行优先  b = np.reshape(a,(3,2),order='C') 改为 b = np.reshape(a,(3,2),order='F')即可

# '''经过验证，utu和vtv，和MATLAB差距在-8之内,可以认为相等'''
# # M_utu = io.loadmat('D:/M_utu.mat')['utu']
# # M_vtv = io.loadmat('D:/M_vtv.mat')['vtv']
# utu = np.reshape(ut, Imosaic.shape, 'F')
# vtv = np.reshape(vt, Imosaic.shape, 'F')

# # print(utu[1990,750:760])
# # print(M_utu[1990,750:760])
# # print(np.min(utu-M_utu['utu']))
# # print(np.min(vtv-M_vtv['vtv']))

# # np.savetxt('D:/utu.txt',utu,fmt='%.4f')
# # np.savetxt('D:/vtv.txt',vtv,fmt='%.4f')


# '''
# 为下面的插值函数griddata做准备
# xy是原图像I1的二维点对
# [[0,0]
#  [0,1]
#  [0,2]
#  ...
#  [767,574]
#  [767,575]]
# xy长度为 768*576 = 442368
# '''
# I1 = I1.astype(np.float)
# x, y = np.mgrid[0:I1.shape[0], 0:I1.shape[1]]
# x, y = x.flatten(), y.flatten()
# xy = [[x[i], y[i]] for i in range(len(x))]
# xy = np.array(xy)


# '''python中Iterp的图像，像是重叠了好几张图像的结果，再检查一下utu和vtv吧'''
# Iterp = griddata(xy, I1.flatten('F'), (utu, vtv), method='cubic')
# # Iterp = Iterp.astype('uint8')
# # nan是<class 'numpy.float64'>
# plt.imshow(Iterp, cmap='gray')
# plt.show()
# [ix, iy] = np.where(Iterp >= 0)
# print(ix)
# vmin, vmax = min(ix), max(ix)
# umin, umax = min(iy), max(iy)
# print(vmin, vmax)
# print(umin, umax)
# Imosaic[extend:extend+I2.shape[0], extend:extend+I2.shape[1]] = I2


# # 遇到透视变换后图像全黑的，需要把M转置一下
# a = cv2.warpPerspective(I1, M.T, (2*extend+I2.shape[1], 2*extend+I2.shape[0]))
# #a = cv2.warpPerspective(I1,M.T,(I1.shape[1],I1.shape[0]))
# # plt.imshow(a, cmap='gray')
# # plt.show()


def find(pic):
    u = []
    v = []
    for ℹ in range(0, pic.shape[0]):
        for j in range(0, pic.shape[1]):
            if pic[i][j] != None:
                u.append(i)
                v.append(j)
    u = np.array(u)
    v = np.array(v)
    return u, v


def interp2(x,y,img,xi,yi):
    """
    x, y: 初始坐标
    img: 待插值图像
    xi, yi： 插值图像坐标

    使用双线性插值实现：
    -----------------------------
    | q11(x1, y1) | q12(x1, y2) |
    -----------------------------
    | q21(x2, y1) | q22(x2, y2) |
    -----------------------------
    f(x, y) = 1/(x2-x1)(y2-y1) * [f(x1,y1)*(x2-x)(y2-y)) + f(x1, y2)*(x2-x)(y-y1) + f(x2, y1)*(x-x1)(y2-y)
                + f(x2, y2)*(x-x1)(y-y1)]
    """

    img_itp = np.ones([len(xi), len(yi)])

    for i in range(len(x)-1):
        for j in range(len(y)-1) :
            y2_y1 = y[j+1] - y[j]
            x2_x1 = x[i+1] - x[i]
            for m in range(int(x[i]), int(x[i+1])):
                for n in range(int(y[j]), int(y[j+1])):
                    # x2 - x, x - x1, ...
                    x2_x = x[i+1] - xi[m]
                    x_x1 = xi[m] - x[i]
                    y2_y = y[j+1] - yi[n]
                    y_y1 = yi[n] - y[j]

                    # q11: img[j, i], q12: img[j, i+1], q21: img[j+1, i], q22: img[j+1, i+1]
                    img_itp[n, m] = (img[j, i] * y2_y * x2_x + \
                                img[j, i+1] * y2_y * x_x1 + \
                                img[j+1, i] * y_y1 * x2_x + \
                                img[j+1, i+1] * y_y1 * x_x1 ) / y2_y1 / x2_x1
 
    return img_itp


def hjw_graymosaic(I1, I2, affmat):
    '''
    input: a pair of source images
    output: a mosaic image based on liniear interplation transformation
    '''
    print("enter hjw_graymosaic")
    r1, c1 = I1.shape[0], I1.shape[1]
    r2, c2 = I2.shape[0], I2.shape[1]
    Imosaic = np.zeros((r2+2*max(r1, c1), c2+2*max(r1, c1)))

    affinemat = affmat.T
    u, v = find(Imosaic)
    v -= max(r1, c1)
    u -= max(r1, c1)
    u, v = np.reshape(u, (-1, 1)), np.reshape(v, (-1, 1))
    # Matlab   A/B  是A乘以B的逆

    # print(affinemat)
    # np.savetxt('u_1.txt',u)
    # np.savetxt('v_1.txt',v)

    utvt = np.dot(np.hstack((u, v, np.ones((v.shape[0], 1)))),
                  np.linalg.inv(affinemat))
    ut = utvt[:, 0]/utvt[:, 2]
    vt = utvt[:, 1]/utvt[:, 2]
    utu = np.reshape(ut, (r2+2*max(r1, c1), c2+2*max(r1, c1)))
    vtv = np.reshape(vt, (r2+2*max(r1, c1), c2+2*max(r1, c1)))
    print(f'utu.shape={utu.shape}')
    print(f'vtv.shape={vtv.shape}')
    # reshape后，utu = (2336,2136)

    # # Iterp = interp2(double(I1), utu, vtv);
    # Iterp = scipy.ndimage.map_coordinates(
    #     I1, [utu.ravel(), vtv.ravel()], order=3, mode='nearest').reshape(vtv.shape)
    # Iterp = interp2(np.array(range(I1.shape[0])),np.array(range(I1.shape[1])),I1, utu, vtv)


    # a = np.array([[1, 2], [2, 3]])
    # interObj = interpolate.interp2d([0, 2], [0, 2], a)
    # rst = interObj(range(3), range(3))
    # print(a)
    # print(rst)
    # print("np.array(range(I1.shape[0]))",np.array(range(I1.shape[0])))
    # print("np.array(range(I1.shape[1]))",np.array(range(I1.shape[1])))
    # print("I1.shape",I1.shape)
    # print("np.min(ut)",np.min(ut))
    # interObj = interpolate.interp2d(np.array(range(I1.shape[1])),np.array(range(I1.shape[0])),I1)
    # Iterp = interObj(np.array(range(int(np.min(ut)),int(np.max(ut)))), np.array(range(int(np.min(vt)),int(np.max(vt)))))




    Iterp = cv2.warpPerspective(I1, affinemat,(c2+2*max(r1, c1), r2+2*max(r1, c1)))
    # Iterp = cv2.warpPerspective(I1,affinemat,utu.shape)

    #图像平移 下、上、右、左平移
    M = np.float32([[1, 0, 0], [0, 1, max(r1, c1)]])
    Iterp = cv2.warpAffine(Iterp, M, (Iterp.shape[1], Iterp.shape[0]))    
    # M = np.float32([[1, 0, 0], [0, 1, -100]])
    # img2 = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))    
    M = np.float32([[1, 0, max(r1, c1)], [0, 1, 0]])
    Iterp = cv2.warpAffine(Iterp, M, (Iterp.shape[1], Iterp.shape[0]))    
    # M = np.float32([[1, 0, -100], [0, 1, 0]])
    # img4 = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    plt.imshow(Iterp,cmap='gray')
    plt.savefig("Iterp_after_interp2.png")
    plt.show()

    vn, un = find(Iterp)
    vmin1 = np.amin(vn)
    vmax1 = np.amax(vn)
    umin1 = np.amin(un)
    umax1 = np.amax(un)

    Imosaic = np.zeros((r2+2*max(r1, c1), c2+2*max(r1, c1)))
    Imosaic[max(r1, c1): max(r1, c1) + r2, max(r1, c1): max(r1, c1) + c2] = I2
    # Imosaic[0: 0 + r2, 0: 0 + c2] = I2


    print(f'Imosaic.shape={Imosaic.shape}')
    print(f'Iterp.shape={Iterp.shape}')
    for i in range( Imosaic.shape[0]-1):
        for j in range( Imosaic.shape[1]-1):
            if (Iterp[i][j]!=None) and (Imosaic[i][j]!=None) :
                Imosaic[i][j] = (Imosaic[i][j] + Iterp[i][j]) / 2
            elif (Iterp[i][j]!=None) and (Imosaic[i][j]==None) :
                Imosaic[i][j] = Iterp[i][j]
    validuv = [min(vmin1, max(r1, c1)), min(umin1, max(r1, c1)), max(
        vmax1, max(r1, c1) + r2), max(umax1, max(r1, c1) + c2)]
    print(f'validuv={validuv}')
    Imosaic=Imosaic[validuv[0] : validuv[2],validuv[1] : validuv[3]]
    plt.imshow(Imosaic,cmap='gray')
    plt.savefig("Imosaic.png")
    plt.show()
    return Imosaic