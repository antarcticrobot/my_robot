# # -- coding: utf-8 --
 
# import sys
# import threading
# import numpy as np
# import termios
# import cv2
# from ctypes import *
 
# sys.path.append("/home/yr/catkin_ws/src/my_robot/scripts/MvImport")
# from MvCameraControl_class import *
 
# g_bExit = False
# flag = False

# img_w=1920
# img_h=1080
# img_c=3

 
# # 这是官方给的线程，只能捕获帧的信息，类似于get one frame: Width[3072], Height[2048], nFrameNum[711]
# # 不能得到帧的数据
# def work_thread(cam=0, pData=0, nDataSize=0):
#     stFrameInfo = MV_FRAME_OUT_INFO_EX()
#     memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
#     while True:
#         ret = cam.MV_CC_GetOneFrameTimeout(pData, nDataSize, stFrameInfo, 1000)
#         if ret == 0:
#             print ("get one frame: Width[%d], Height[%d], nFrameNum[%d]"  % (stFrameInfo.nWidth, stFrameInfo.nHeight, stFrameInfo.nFrameNum))
#         else:
#             print ("no data[0x%x]" % ret)
#         if g_bExit == True:
#                 break


# # 自己在这个线程中修改，可以将相机获得的数据转换成opencv支持的格式，然后再用opencv操作
# def work_thread2(cam=0, pData=0, nDataSize=0):
#     global flag
#     stFrameInfo = MV_FRAME_OUT_INFO_EX()
#     memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))

#     while True:
#         ret = cam.MV_CC_GetOneFrameTimeout(pData, nDataSize, stFrameInfo, 1000)
#         print('----', stFrameInfo.enPixelType)
#         if ret == 0:  
#             temp = np.asarray(pData).reshape((1080, 1920, 3))  # 根据自己分辨率进行转化
#             temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)  # 这一步获取到的颜色不对，因为默认是BRG，要转化成RGB，颜色才正常
#             cv2.namedWindow("ori", cv2.WINDOW_NORMAL)
#             cv2.imshow("ori", temp)

#             gray = cv2.cvtColor(temp,cv2.COLOR_BGR2GRAY)
#             ret,binary = cv2.threshold(gray,130,255,cv2.THRESH_BINARY)
#             cv2.namedWindow("binary", cv2.WINDOW_NORMAL)
#             cv2.imshow('binary',binary)
#             cv2.waitKey(1) 
            
#             # if cv2.waitKey(1) & 0xFF == ord('q'):
#             #     break
#         else:
#             print("no data[0x%x]" % ret)
#         if g_bExit == True:
#             break 
        
# def press_any_key_exit():
#     fd = sys.stdin.fileno()
#     old_ttyinfo = termios.tcgetattr(fd)
#     new_ttyinfo = old_ttyinfo[:]
#     new_ttyinfo[3] &= ~termios.ICANON
#     new_ttyinfo[3] &= ~termios.ECHO
#     termios.tcsetattr(fd, termios.TCSANOW, new_ttyinfo)
#     try:
#         os.read(fd, 7)
#     except:
#         pass
#     finally:
#         termios.tcsetattr(fd, termios.TCSANOW, old_ttyinfo)


# if __name__ == "__main__":
 
#     # rospy.init_node("listener_p")
#     # sub = rospy.Subscriber("chatter",String,doMsg,queue_size=10)

#     SDKVersion = MvCamera.MV_CC_GetSDKVersion()
#     print ("SDKVersion[0x%x]" % SDKVersion)
 
#     deviceList = MV_CC_DEVICE_INFO_LIST()
#     tlayerType = MV_GIGE_DEVICE | MV_USB_DEVICE
     
#     # ch:枚举设备 | en:Enum device
#     ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
#     if ret != 0:
#         print ("enum devices fail! ret[0x%x]" % ret)
#         sys.exit()
 
#     if deviceList.nDeviceNum == 0:
#         print ("find no device!")
#         sys.exit()
 
#     print ("Find %d devices!" % deviceList.nDeviceNum)
 
#     for i in range(0, deviceList.nDeviceNum):
#         mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
#         if mvcc_dev_info.nTLayerType == MV_GIGE_DEVICE:
#             print ("\ngige device: [%d]" % i)
#             strModeName = ""
#             for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
#                 strModeName = strModeName + chr(per)
#             print ("device model name: %s" % strModeName)
 
#             nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
#             nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
#             nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
#             nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)
#             print ("current ip: %d.%d.%d.%d\n" % (nip1, nip2, nip3, nip4))
#         elif mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
#             print ("\nu3v device: [%d]" % i)
#             strModeName = ""
#             for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
#                 if per == 0:
#                     break
#                 strModeName = strModeName + chr(per)
#             print ("device model name: %s" % strModeName)
 
#             strSerialNumber = ""
#             for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
#                 if per == 0:
#                     break
#                 strSerialNumber = strSerialNumber + chr(per)
#             print ("user serial number: %s" % strSerialNumber)
 
#     nConnectionNum = 0
#     if int(nConnectionNum) >= deviceList.nDeviceNum:
#         print ("intput error!")
#         sys.exit()
 
#     # ch:创建相机实例 | en:Creat Camera Object
#     cam = MvCamera()
     
#     # ch:选择设备并创建句柄| en:Select device and create handle
#     stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
 
#     ret = cam.MV_CC_CreateHandle(stDeviceList)
#     if ret != 0:
#         print ("create handle fail! ret[0x%x]" % ret)
#         sys.exit()
 
#     # ch:打开设备 | en:Open device
#     ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
#     if ret != 0:
#         print ("open device fail! ret[0x%x]" % ret)
#         sys.exit()
     
#     # ch:探测网络最佳包大小(只对GigE相机有效) | en:Detection network optimal package size(It only works for the GigE camera)
#     if stDeviceList.nTLayerType == MV_GIGE_DEVICE:
#         nPacketSize = cam.MV_CC_GetOptimalPacketSize()
#         if int(nPacketSize) > 0:
#             ret = cam.MV_CC_SetIntValue("GevSCPSPacketSize",nPacketSize)
#             if ret != 0:
#                 print ("Warning: Set Packet Size fail! ret[0x%x]" % ret)
#         else:
#             print ("Warning: Get Packet Size fail! ret[0x%x]" % nPacketSize)
 
#     # ch:设置触发模式为off | en:Set trigger mode as off
#     ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
#     if ret != 0:
#         print ("set trigger mode fail! ret[0x%x]" % ret)
#         sys.exit()
 
#     # ch:获取数据包大小 | en:Get payload size
#     stParam =  MVCC_INTVALUE()
#     memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
     
#     ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
#     if ret != 0:
#         print ("get payload size fail! ret[0x%x]" % ret)
#         sys.exit()
#     nPayloadSize = stParam.nCurValue
 
#     # ch:开始取流 | en:Start grab image
#     ret = cam.MV_CC_StartGrabbing()
#     if ret != 0:
#         print ("start grabbing fail! ret[0x%x]" % ret)
#         sys.exit()
#     #将PayloadSize的uint数据转为可供numpy处理的数据，后面就可以用numpy将其转化为numpy数组格式。
#     data_buf = (c_ubyte * nPayloadSize)()
 
#     try:
#         #有些代码可能会在data_buf前面加上byteref，如果这样做的话，就会将数据转为浮点型，
#         # 而opencv需要的是整型，会报错，所以这里就不需要转化了
#         #hThreadHandle = threading.Thread(target=work_thread_rgb82bgr, args=(cam, byref(data_buf), nPayloadSize))
#         hThreadHandle = threading.Thread(target=work_thread2, args=(cam, data_buf, nPayloadSize))
#         hThreadHandle.start()
#     except:
#         print ("error: unable to start thread")
         
#     print ("press a key to stop grabbing.")
#     press_any_key_exit()
 
#     g_bExit = True
#     hThreadHandle.join()
 
#     # ch:停止取流 | en:Stop grab image
#     ret = cam.MV_CC_StopGrabbing()
#     if ret != 0:
#         print ("stop grabbing fail! ret[0x%x]" % ret)
#         del data_buf
#         sys.exit()
 
#     # ch:关闭设备 | Close device
#     ret = cam.MV_CC_CloseDevice()
#     if ret != 0:
#         print ("close deivce fail! ret[0x%x]" % ret)
#         del data_buf
#         sys.exit()
 
#     # ch:销毁句柄 | Destroy handle
#     ret = cam.MV_CC_DestroyHandle()
#     if ret != 0:
#         print ("destroy handle fail! ret[0x%x]" % ret)
#         del data_buf
#         sys.exit()
 
#     del data_buf
