# infrared and visible images registration,  The whole work is divided into 5 parts

# 带着问题：
# 1.descriptor和主方向angle有什么区别
# 2.如果说最后只要一个 transform matrix 即可，那么为什么要那么多对匹配点呢?
# 3.为什么一定要找到curve再算主方向呢？为什么不是curve就不行呢？   短的canny检测出来的离散点，她认为不算做curve

# 基本库
import numpy as np
import cv2
import matplotlib.pyplot as plt

# 自定义函数
from hjw_readimage import *
from hjw_resizeImage import *
from hjw_registration import hjw_registration
from hjw_getAffine import hjw_getAffine

from hjw_subpixelFine import hjw_subpixelFine
from hjw_graymosaic import hjw_graymosaic
from hjw_rgbmosaic import hjw_rgbmosaic
from helper import get_time

# source image path
path_infrared = '/home/yr/catkin_ws/src/my_robot/matlab/Image-registration/CAO-C2F/Example_Images/'
path_visible = '/home/yr/catkin_ws/src/my_robot/matlab/Image-registration/CAO-C2F/Example_Images/'

class Registration:
	def __init__(self, args1,args2):
		self.img_infrared = args1
		self.img_visible = args2
		

	def prepare_and_compute(self):
		# %%
		# section 1: Read source images
		# 这里省略了张正友畸变校正法，去除红外图片的畸变
		I1_rgb, I1_gray, I2_rgb, I2_gray = readimage(
			path_infrared, img_infrared, path_visible, img_visible)
		print('【Successfully read image!!】')

		# %%
		# section 2: Resize images based on the minimum imaclosege height
		I1, I2, scale = resizeImage(I1_gray, I2_gray)
		I1_itea = I1

		# %%
		# section 3: Registrate iteratively & Coarse matching

		iterationNum = 1
		iteration = 0
		Runtime = 0
		maxRMSE = 4*np.ceil(I2.shape[0]/300)  # maxRMSE = 12.0
		AffineTrans = np.zeros((3, 3, iterationNum))

		while iteration < iterationNum:
			[P1, P2, Rt, corner12, pos_cor1] = hjw_registration(
				I1_itea, I2, maxtheta=20, maxErr=maxRMSE, iteration=iteration, zoomascend=1, zoomdescend=0, Lc=6, showflag=1, I2ori=I2_gray)
			Runtime += Rt

			I1_itea, affmat = hjw_getAffine(
				I1_itea, I2, P1, P2)  # % [v1,u1]==[v2,u2]
			AffineTrans[:, :, iteration] = affmat.T
			iteration += 1

		# % Points of I1gray after resize
		# Matlab中，拼接后P1 是 (98,3) corner12是(2972,2)
		P1 = np.hstack((P1, np.ones((P1.shape[0], 1))))
		P1 = P1[:, 0:2]
		corner12 = corner12[:, 0:2]

		# % Correct matches in the source images
		P1[:, 1] = I1_gray.shape[0]/2 + scale[0] * (P1[:, 1] - I1.shape[0]/2)
		P1[:, 0] = I1_gray.shape[1]/2 + scale[0] * (P1[:, 0] - I1.shape[1]/2)
		corner12[0:pos_cor1, 1] = I1_gray.shape[0]/2 + \
			scale[0] * (corner12[0:pos_cor1, 1] - I1.shape[0]/2)
		corner12[0:pos_cor1, 0] = I1_gray.shape[1]/2 + \
			scale[0] * (corner12[0:pos_cor1, 0] - I1.shape[1]/2)

		P2[:, 1] = I2_gray.shape[0]/2 + scale[1] * (P2[:, 1] - I2.shape[0]/2)
		P2[:, 0] = I2_gray.shape[1]/2 + scale[1] * (P2[:, 0] - I2.shape[1]/2)
		corner12[pos_cor1+1:, 1] = I2_gray.shape[0]/2 + \
			scale[1] * (corner12[pos_cor1+1:, 1] - I2.shape[0]/2)
		corner12[pos_cor1+1:, 0] = I2_gray.shape[1]/2 + \
			scale[1] * (corner12[pos_cor1+1:, 0] - I2.shape[1]/2)

		# %%
		# section 4: Fine matching
		P3 = hjw_subpixelFine(P1, P2)

		# %%
		# section 5: Show visual registration result
		_, affmat = hjw_getAffine(I1_gray, I2_gray, P1, P3)
		affmat = affmat.T
		print(f'affmat={affmat}')
		# affmat = np.array([[0.2119,	-1.0724,	2.0265e-04],[1.1479,	0.1401,	-6.4305e-05],[-228.4349,	743.9051,	1]])

		Imosaic = hjw_graymosaic(I1_gray, I2_gray, affmat)

		print(f'I1_rgb.shape={I1_rgb.shape}')
		rgb_Imosaic = hjw_rgbmosaic(I1_rgb, I2_rgb, affmat)
		rgb_Imosaic = rgb_Imosaic[..., ::-1]
		cv2.imwrite("result.jpg", rgb_Imosaic)

		# plt.imshow(rgb_Imosaic.astype('uint8'))
		# plt.savefig('./tmp/main_'+get_time()+'.png')
		# plt.close()
		# plt.show()



if __name__ == '__main__':

    img_infrared = 'I1.jpg'
    img_visible = 'V1.jpg'

    r = Registration(img_infrared,img_visible)
    r.prepare_and_compute()
