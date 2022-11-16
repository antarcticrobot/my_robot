

from math import nan
import scipy
from scipy import io
import numpy as np
from scipy import interpolate
from scipy.interpolate import griddata
import cv2
import matplotlib.pyplot as plt


# Matlab的.T不是转置的意思，而是取出T属性'''
# u, v = u.flatten('F'), v.flatten('F')
# Matlab重排时，列优先
# python重排时，行优先  b = np.reshape(a,(3,2),order='C') 改为 b = np.reshape(a,(3,2),order='F')即可
# 遇到透视变换后图像全黑的，需要把M转置一下


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


def hjw_graymosaic(I1, I2, affmat):
    '''
    input: a pair of source images
    output: a mosaic image based on liniear interplation transformation
    '''
    # print("enter hjw_graymosaic")
    r1, c1 = I1.shape[0], I1.shape[1]
    r2, c2 = I2.shape[0], I2.shape[1]
    Imosaic = np.zeros((r2+2*max(r1, c1), c2+2*max(r1, c1)))

    affinemat = affmat.T
    u, v = find(Imosaic)
    v -= max(r1, c1)
    u -= max(r1, c1)
    u, v = np.reshape(u, (-1, 1)), np.reshape(v, (-1, 1))
    # Matlab   A/B  是A乘以B的逆

    utvt = np.dot(np.hstack((u, v, np.ones((v.shape[0], 1)))),
                  np.linalg.inv(affinemat))
    ut = utvt[:, 0]/utvt[:, 2]
    vt = utvt[:, 1]/utvt[:, 2]
    utu = np.reshape(ut, (r2+2*max(r1, c1), c2+2*max(r1, c1)))
    vtv = np.reshape(vt, (r2+2*max(r1, c1), c2+2*max(r1, c1)))
    print(f'utu.shape={utu.shape}')
    print(f'vtv.shape={vtv.shape}')
    # reshape后，utu = (2336,2136)

    Iterp = cv2.warpPerspective(
        I1, affinemat, (c2+2*max(r1, c1), r2+2*max(r1, c1)))
    # Iterp = cv2.warpPerspective(I1,affinemat,utu.shape)

    # 图像平移 下、上、右、左平移
    M = np.float32([[1, 0, max(r1, c1)], [0, 1, max(r1, c1)]])
    Iterp = cv2.warpAffine(Iterp, M, (Iterp.shape[1], Iterp.shape[0]))

    vn, un = find(Iterp)
    vmin1 = np.amin(vn)
    vmax1 = np.amax(vn)
    umin1 = np.amin(un)
    umax1 = np.amax(un)

    Imosaic = np.zeros((r2+2*max(r1, c1), c2+2*max(r1, c1)))
    Imosaic[max(r1, c1): max(r1, c1) + r2, max(r1, c1): max(r1, c1) + c2] = I2

    # print(f'Imosaic.shape={Imosaic.shape}')
    # print(f'Iterp.shape={Iterp.shape}')
    for i in range(Imosaic.shape[0]-1):
        for j in range(Imosaic.shape[1]-1):
            if (Iterp[i][j] != None) and (Imosaic[i][j] != None):
                Imosaic[i][j] = (Imosaic[i][j] + Iterp[i][j]) / 2
            elif (Iterp[i][j] != None) and (Imosaic[i][j] == None):
                Imosaic[i][j] = Iterp[i][j]
    validuv = [min(vmin1, max(r1, c1)), min(umin1, max(r1, c1)), max(
        vmax1, max(r1, c1) + r2), max(umax1, max(r1, c1) + c2)]
    # print(f'validuv={validuv}')
    Imosaic = Imosaic[validuv[0]: validuv[2], validuv[1]: validuv[3]]
    return Imosaic
