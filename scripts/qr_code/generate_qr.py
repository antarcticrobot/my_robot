#!/usr/bin/env python 
# -*- coding:utf-8 -*-

'''
生成二维码
'''

import qrcode

# 二维码包含的示例数据
data = "https://www.python.org/https://www.python.org/"
# 生成的二维码图片名称
filename = "python.png"
# 生成二维码
img = qrcode.make(data)
# 保存成图片输出
img.save(filename)
