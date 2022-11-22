import os
import sys
import cv2

os.chdir('/home/yr/catkin_ws/src/my_robot')
sys.path.append('./scripts/multiple_image_stitching/code/' ) # 更改当前工作目录
from pano import Stitch

args = "./scripts/multiple_image_stitching/code/txtlists/files5.txt"
print ("Parameters : ", args)
s = Stitch(args)
s.leftshift()
s.rightshift()
print ("done")
cv2.imwrite("test12.jpg", s.leftImage)
print ("image written")
cv2.destroyAllWindows()