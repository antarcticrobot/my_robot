import numpy as np

# Set the target temp range here
min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius


def show_temperature_distribution(img, x, y, w, h):
    # g = np.mean(img[x:x+w, y:y+h])
    # print('avg of roi', g, map_g_to_temp(g))
    print((img.shape))
    print(0, x, y, y+h)
    print(x, x+w, y, y+h)
    print(x+w, 120, y, y+h)

    tmpArr = img[y:y+h, 0:x]
    g = np.mean(tmpArr)
    ans1 = map_g_to_temp(g)
    if (w > 0 and h > 0):
        tmpArr = img[y:y+h, x:x+w]
        g = np.mean(tmpArr)
        ans2 = map_g_to_temp(g)
    else:
        ans2 = None
    if (x+w < 120):
        tmpArr = img[y:y+h, x+w:120]
        g = np.mean(tmpArr)
        ans3 = map_g_to_temp(g)
    else:
        ans3 = None

    # g = np.mean(img[:][0:y])
    # print('avg of roi', g, map_g_to_temp(g))
    # g = np.mean(img[:][y:y+h])
    # print('avg of roi', g, map_g_to_temp(g))
    # g = np.mean(img[:][y+h:160])
    # print('avg of roi', g, map_g_to_temp(g))

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
        objType = str(CornerNum)+"polygon"  # "Circle"
    else:
        objType = "N"
    return objType
