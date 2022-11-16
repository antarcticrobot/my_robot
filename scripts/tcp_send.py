import socket
import time
import os

client_addr = ('10.10.100.254',8899)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(client_addr)

suffixList=('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')
def get_img_file(directionName):
        imagelist = []
        for parent, dirnames, filenames in os.walk(directionName):
            for filename in filenames:
                if filename.lower().endswith(suffixList):
                    imagelist.append(os.path.join(parent, filename))
            return imagelist

def send_file(filename):
    fname1, fname2 = os.path.split(filename)
    with open(filename, 'rb') as f:
        s.send(b"\xFF\x5A\x02")
        s.send(len(fname2).to_bytes(2, byteorder="little", signed=True))
        s.send(fname2.encode())
        a = f.read()
        file_total_size = len(a)
        send_size = 0
        while send_size < file_total_size:
            cur_size = min(500, file_total_size - send_size)
            s.send(b"\xFF\x5A\x03")
            s.send(cur_size.to_bytes(2, byteorder="little", signed=True))
            s.send(a[send_size:send_size + cur_size])
            send_size += cur_size
            time.sleep(0.01)
        print("发送完成，共发送字节数：", send_size)


while True:
    current_path = os.path.dirname(__file__)
    inDir = os.path.join(current_path, 'input/')

    imagelist = get_img_file(inDir)
    if imagelist is None:
        print("imagelist is None")
        continue
    else:
        count = len(imagelist)
        for picName in imagelist:
            send_file(picName)
            count = count-1
        s.send(b"\xFF\x5A\x04\x00\x00")
        print('已发送 ', ' end')
        break
s.close