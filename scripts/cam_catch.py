# -- coding: utf-8 --

import sys
import os
import datetime
import cv2
import numpy as np
import rospy
from ctypes import *
from std_msgs.msg import String
from my_robot.msg import msg_for_cam

sys.path.append("/home/yr/catkin_ws/src/my_robot/scripts/MvImport")
from MvCameraControl_class import *

img_w = 1920
img_h = 1080
img_c = 3
cam = None
data_buf = None
nPayloadSize = None


def get_and_process_img(imgLoc, stFrameInfo, cam=0, pData=0, nDataSize=0):
    ret = cam.MV_CC_GetOneFrameTimeout(pData, nDataSize, stFrameInfo, 1000)
    if ret == 0:
        temp = np.asarray(pData).reshape((img_h, img_w, img_c))
        temp = cv2.cvtColor(temp, cv2.COLOR_BGR2RGB)
        now = datetime.datetime.now()
        filepath = "/home/yr/MVS_Pictures/"
        filepath += datetime.datetime.strftime(now, '%Y-%m-%d')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename = datetime.datetime.strftime(now, '%Y-%m-%d-%H-%M-%S')
        filename += imgLoc
        cv2.imwrite(filepath + "/" + filename + ".jpg", temp)
    else:
        print("no data[0x%x]" % ret)


def doMsg(msg):
    if (str.find(msg.mode, "LOC") >= 0):
        print(msg.mode, msg.x, msg.z, msg.w)
        imgLoc = "_%d_%d_%d" % (msg.x, msg.z, msg.w)

        stFrameInfo = MV_FRAME_OUT_INFO_EX()
        memset(byref(stFrameInfo), 0, sizeof(stFrameInfo))
        get_and_process_img(imgLoc, stFrameInfo, cam, data_buf, nPayloadSize)


def prepare_cam():
    global cam, data_buf, nPayloadSize

    deviceList = MV_CC_DEVICE_INFO_LIST()
    tlayerType = MV_USB_DEVICE
    ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
    if ret != 0:
        print("enum devices fail! ret[0x%x]" % ret)
        sys.exit()
    if deviceList.nDeviceNum == 0:
        print("find no device!")
        sys.exit()
    print("Find %d devices!" % deviceList.nDeviceNum)

    for i in range(0, deviceList.nDeviceNum):
        mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(
            MV_CC_DEVICE_INFO)).contents
        if mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
            print("\nu3v device: [%d]" % i)
            strModeName = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                if per == 0:
                    break
                strModeName = strModeName + chr(per)
            print("device model name: %s" % strModeName)

            strSerialNumber = ""
            for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                if per == 0:
                    break
                strSerialNumber = strSerialNumber + chr(per)
            print("user serial number: %s" % strSerialNumber)

    nConnectionNum = 0
    if int(nConnectionNum) >= deviceList.nDeviceNum:
        print("no cam error!")
        sys.exit()

    cam = MvCamera()
    stDeviceList = cast(deviceList.pDeviceInfo[int(
        nConnectionNum)], POINTER(MV_CC_DEVICE_INFO)).contents
    ret = cam.MV_CC_CreateHandle(stDeviceList)
    if ret != 0:
        print("create handle fail! ret[0x%x]" % ret)
        sys.exit()

    ret = cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
    if ret != 0:
        print("open device fail! ret[0x%x]" % ret)
        sys.exit()

    ret = cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
    if ret != 0:
        print("set trigger mode fail! ret[0x%x]" % ret)
        sys.exit()

    stParam = MVCC_INTVALUE()
    memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
    ret = cam.MV_CC_GetIntValue("PayloadSize", stParam)
    if ret != 0:
        print("get payload size fail! ret[0x%x]" % ret)
        sys.exit()
    nPayloadSize = stParam.nCurValue

    ret = cam.MV_CC_StartGrabbing()
    if ret != 0:
        print("start grabbing fail! ret[0x%x]" % ret)
        sys.exit()

    data_buf = (c_ubyte * nPayloadSize)()


def close_and_clear_cam():
    global cam, data_buf, nPayloadSize

    ret = cam.MV_CC_StopGrabbing()
    if ret != 0:
        print("stop grabbing fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    ret = cam.MV_CC_CloseDevice()
    if ret != 0:
        print("close deivce fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    ret = cam.MV_CC_DestroyHandle()
    if ret != 0:
        print("destroy handle fail! ret[0x%x]" % ret)
        del data_buf
        sys.exit()

    del data_buf


if __name__ == "__main__":
    prepare_cam()

    rospy.init_node("listener_p")
    sub = rospy.Subscriber("cam_flag_with_pos", msg_for_cam,
                           doMsg, queue_size=10)
    rospy.spin()

    # 不会运行到这里。没想好cam的清理应该放到哪里。
    close_and_clear_cam()
