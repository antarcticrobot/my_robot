#!/usr/bin/python
# -*-coding: utf-8 -*-

import socket
import threading
import struct
import os
import numpy as np
import time


class SerialSocket:
    def __init__(self, ip, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))

    def read_data(self):
        global is_exit
        global data_bytes
        while not is_exit:
            rec_str = self.s.recv(1024)
            count = len(rec_str)
            if count > 0:
                data_bytes = data_bytes + rec_str


ip = '10.10.100.254'
port = 8899
is_exit = False
data_bytes = bytearray()

file_name1 = "tmp.jpg"
file1 = open(file_name1, 'wb')

if __name__ == '__main__':
    outDir = os.path.join(os.path.dirname(__file__), 'output2/')

    mSocket = SerialSocket(ip, port)
    t1 = threading.Thread(target=mSocket.read_data)
    t1.setDaemon(True)
    t1.start()
    countTmp = 0

    while not is_exit:
        data_len = len(data_bytes)
        print("data_len",data_len)
        i = 0
        while i <= data_len - 5:
            if data_bytes[i] == 0xFF and data_bytes[i + 1] == 0x5A:
                frame_code = data_bytes[i + 2]
                frame_len = struct.unpack('<H', data_bytes[i + 3:i + 5])[0]
                if i + 5 + frame_len <= data_len:
                    data = data_bytes[i + 5:i + 5 + frame_len]
                    if frame_code == 0x02:
                        file1.close()
                        file_name1 = str(data.decode())
                        file1 = open(outDir + file_name1, 'wb')
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
                        time.sleep(5)
                        exit(0)
                    i = i + 5 + frame_len
                else:
                    break
            else:
                i = i + 1
        data_bytes[0:i] = b''