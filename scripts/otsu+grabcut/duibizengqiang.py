import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

# 计算局部均值和标准差
def local_mean_stddv(input_img, x, y):
    img=[[] for i in range(3)]
    for i in range(3):
        for j in range(3):
            img[i].append(input_img[x-1+i][y-1+j])
    img_np = np.array(img)
    (mean , stddv) = cv.meanStdDev(img_np)
    return mean, stddv

# 使用直方图统计量增强局部图像
def HistogramStatisticsEnhance(input_img):
    # 初始化
    output_image = input_img
    # 定义参数
    k0 = 0
    k1 = 0.25
    k2 = 0
    k3 = 0.1
    C = 20
    # 创建空列表
    means = [[] for i in range(512)]
    stddvs = [[] for i in range(512)]
    # 计算全局均值和标准差
    (m_G, sigma_G) = cv.meanStdDev(input_img)
    # 计算每个元素的 3 邻域的均值与标准差
    for i in range(0, 512):
        for j in range(0, 512):
            (mean, stddv) = local_mean_stddv(input_img, i+1, j+1)
            means[i].append(mean)
            stddvs[i].append(stddv)
    # 代入分段函数
    for i in range(0, 512):
        for j in range(0, 512):
            if (k0*m_G <= means[i][j] and means[i][j] <= k1*m_G) and (k2*sigma_G <= stddvs[i][j] and stddvs[i][j] <= k3*sigma_G):
                output_image[i, j] = C*input_img[i][j]
    return output_image
            
def main():
    # 读取图片
    src = cv.imread("/home/yr/热成像数据_存档_排烟管/2023_02_20_1630_pyg/raw/421802.bmp")
    # 转化为灰度图
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 显示灰度图
    cv.imshow("gray image", gray) 
    # 绘制直方图
    plt.hist(gray.ravel(),256,[0,256]); plt.show()
    # 扩充边界，cv.BORDER_REPLICATE：使用最边界的像素值代替
    gray1 = cv.copyMakeBorder(gray,1,1,1,1,cv.BORDER_REPLICATE)
    # 使用直方图统计量增强局部图像
    # gray1.dtype = "float16"
    enhanced_img = HistogramStatisticsEnhance(gray1)
    # 显示使用直方图统计量增强局部的图像
    cv.imshow("enhanced_img", enhanced_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite("enhanced_img.tif", enhanced_img)

if __name__ == "__main__":
    main()
