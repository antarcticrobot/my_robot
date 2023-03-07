#!/usr/bin/python
# -*-coding: utf-8 -*-

import serial

readPort = "/dev/openmvcam"
baudRate = 57600

port = serial.Serial(readPort, baudRate)
port.open()

count = port.inWaiting()
if count > 0:
    print(port.read(count))