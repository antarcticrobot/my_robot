import sys
import cv2

sys.path.append('./scripts/multiple_image_stitching/code/' ) # 更改当前工作目录
from pano import Stitch

args = "./scripts/multiple_image_stitching/code/txtlists/files1.txt"
print ("Parameters : ", args)
s = Stitch(args)
s.leftshift()
s.rightshift()
print ("done")
cv2.imwrite("test12.jpg", s.leftImage)
print ("image written")
cv2.destroyAllWindows()