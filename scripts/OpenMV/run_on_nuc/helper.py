import numpy as np

# Set the target temp range here
min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius


def show_temperature_distribution(img, x, y, w, h):
    if (h <= 0):
        return None, None, None
    if (x > 0):
        tmpArr = img[y:y+h, 0:x]
        ans1 = map_g_to_temp(np.mean(tmpArr))
    else:
        ans1 = None
    if (w > 0):
        tmpArr = img[y:y+h, x:x+w]
        ans2 = map_g_to_temp(np.mean(tmpArr))
    else:
        ans2 = None
    if (x+w < 120):
        tmpArr = img[y:y+h, x+w:120]
        ans3 = map_g_to_temp(np.mean(tmpArr))
    else:
        ans3 = None
    return ans1, ans2, ans3


def get_shape_name(CornerNum, w, h):
    if CornerNum == 3:
        objType = "triangle"
    elif CornerNum == 4:
        if w == h:
            objType = "Square"
        else:
            objType = "Rectangle"
    elif CornerNum > 4:
        objType = str(CornerNum)+" polygon"
    else:
        objType = "N"
    return objType
