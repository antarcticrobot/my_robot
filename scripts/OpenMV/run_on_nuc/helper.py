import numpy as np

# Set the target temp range here
min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius


def show_temperature_distribution(img, x, y, w, h):
    g = np.mean(img[x:x+w, y:y+h])
    print('avg of roi', g, map_g_to_temp(g))

    g = np.mean(img[0:x])
    print('avg of roi', g, map_g_to_temp(g))
    g = np.mean(img[x:x+w])
    print('avg of roi', g, map_g_to_temp(g))
    g = np.mean(img[x+w:120])
    print('avg of roi', g, map_g_to_temp(g))

    g = np.mean(img[:][0:y])
    print('avg of roi', g, map_g_to_temp(g))
    g = np.mean(img[:][y:y+h])
    print('avg of roi', g, map_g_to_temp(g))
    g = np.mean(img[:][y+h:160])
    print('avg of roi', g, map_g_to_temp(g))


def get_shape_name(CornerNum, w, h):
    if CornerNum == 3:
        objType = "triangle"
    elif CornerNum == 4:
        if w == h:
            objType = "Square"
        else:
            objType = "Rectangle"
    elif CornerNum > 4:
        objType = "Circle"
    else:
        objType = "N"
    return objType