#!/usr/bin/env python
# -*- coding:utf-8 -*-

import qrcode


def generate_qr_code(data, filename):
    img = qrcode.make(data)
    img.save(filename)


if __name__ == "__main__":
    data = "height_01"
    filename = "python.png"
    generate_qr_code(data, filename)
