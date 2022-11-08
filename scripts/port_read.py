#!/usr/bin/python
# -*-coding: utf-8 -*-

import serial
import threading
import struct
import os
import numpy as np
import time
# from port_send import send_dictionary


class SerialPort:
    def __init__(self, port, buand):
        self.port = serial.Serial(port, buand)
        self.port.close()
        if not self.port.isOpen():
            self.port.open()

    def read_data(self):
        global is_exit
        global data_bytes
        while not is_exit:
            count = self.port.inWaiting()
            if count > 0:
                rec_str = self.port.read(count)
                data_bytes = data_bytes + rec_str


readPort = "/dev/ttyUSB0"
baudRate = 57600
is_exit = False
data_bytes = bytearray()

file_name1 = "tmp.jpg"
file1 = open(file_name1, 'wb')

if __name__ == '__main__':
    outDir = os.path.join(os.path.dirname(__file__), 'output/')

    mSerial = SerialPort(readPort, baudRate)
    t1 = threading.Thread(target=mSerial.read_data)
    t1.setDaemon(True)
    t1.start()
    countTmp = 0

    while not is_exit:
        data_len = len(data_bytes)
        i = 0
        while (i <= data_len-5):
            if (data_bytes[i] == 0xFF and data_bytes[i + 1] == 0x5A):
                frame_code = data_bytes[i + 2]
                frame_len = struct.unpack('<H', data_bytes[i + 3:i + 5])[0]
                if(i+5+frame_len <= data_len):
                    data=data_bytes[i + 5:i+5+frame_len]
                    if frame_code == 0x02:
                        file1.close()
                        file_name1=str(data.decode())
                        file1 = open(outDir+file_name1, 'wb')
                        print("重置计数前，共接收字节数： ", countTmp)
                        countTmp = 0
                    if frame_code == 0x03:
                        try:
                            image_array = np.frombuffer(data, dtype=np.uint8)
                            image_array.tofile(file1)
                            countTmp += len(data)
                        except Exception as e:
                            raise e
                    if frame_code == 0x04:
                        print("Received 0x04")
                        print("接收完成，共接收字节数： ", countTmp)
                        print("开始 send_dictionary()")
                        time.sleep(0.05)
                        # send_dictionary(outDir, mSerial.port)
                        print("结束 send_dictionary()")
                        exit(0)
                    i = i + 5 + frame_len
                else:
                    break
            else:
                i = i + 1
        data_bytes[0:i] = b''