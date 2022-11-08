import serial
import time
import os
# from helper import *

suffixList=('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')
def get_img_file(directionName):
        imagelist = []
        for parent, dirnames, filenames in os.walk(directionName):
            for filename in filenames:
                if filename.lower().endswith(suffixList):
                    imagelist.append(os.path.join(parent, filename))
            return imagelist

def send_file(filename, mPort):
    fname1, fname2 = os.path.split(filename)
    if mPort.is_open:
        with open(filename, 'rb') as f:
            mPort.write([0xFF, 0x5A, 0x02])
            mPort.write(len(fname2).to_bytes(2, byteorder="little", signed=True))
            mPort.write(fname2.encode())
            a = f.read()
            file_total_size = len(a)
            send_size = 0
            while send_size < file_total_size:
                cur_size = min(50, file_total_size - send_size)
                mPort.write([0xFF, 0x5A, 0x03])
                mPort.write((cur_size).to_bytes(2, byteorder="little", signed=True))
                mPort.write(a[send_size:send_size + cur_size])
                send_size += cur_size
                time.sleep(0.01)
            print("发送完成，共发送字节数：", send_size)


def send_dictionary(dictionaryName, mPort):
    imagelist = get_img_file(dictionaryName)
    count = len(imagelist)
    for picName in imagelist:
        send_file(picName, mPort)
        count = count - 1
    mPort.write([0xFF, 0x5A, 0x04, 0x00, 0x00])
    print('已发送 ', ' 0x04')


#readPort = "COM3"
readPort = "/dev/ttyUSB0"

if __name__ == '__main__':
    mPort = serial.Serial(readPort, 57600, bytesize=8, timeout=0.5)
    send_dictionary("/home/yr/catkin_ws/src/my_robot/scripts/input", mPort)