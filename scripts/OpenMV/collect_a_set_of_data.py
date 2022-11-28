
import sensor
import image
import time
import pyb
import utime

min_temp_in_celsius = -10.0
max_temp_in_celsius = 60.0

sensor.reset()
sensor.ioctl(sensor.IOCTL_LEPTON_SET_MEASUREMENT_MODE, True)
sensor.ioctl(sensor.IOCTL_LEPTON_SET_MEASUREMENT_RANGE,
             min_temp_in_celsius, max_temp_in_celsius)

width = sensor.ioctl(sensor.IOCTL_LEPTON_GET_WIDTH)
height = sensor.ioctl(sensor.IOCTL_LEPTON_GET_HEIGHT)
print("Lepton Res (%dx%d)" % (width, height))
print("Radiometry Available: " +
      ("Yes" if sensor.ioctl(sensor.IOCTL_LEPTON_GET_RADIOMETRY) else "No"))

sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=5000)
clock = time.clock()


def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius


def get_time():
    now = pyb.millis()
    return now


filepath = "./2022_11_28_1030_tqyb15"
#filepath = "."

# Color Tracking Thresholds (Grayscale Min, Grayscale Max)
# 145对应30摄氏度，200对应45摄氏度
threshold_list = [(200, 255)]


def compute(img, rect):
    m = img.get_statistics(thresholds=threshold_list, roi=rect).mean()
    ans = map_g_to_temp(m)
    return ans


def save_as_four_format(fileName):
    img.save(fileName+".bmp")
    img.save(fileName+".pgm")
    img.save(fileName+".jpg")
    img.save(fileName+".jpeg")


while (True):
    clock.tick()
    tmp_name = str(get_time())
    img = sensor.snapshot()
    save_as_four_format(filepath+'/raw/'+tmp_name)

    blob_stats = []
    blobs = img.find_blobs(
        threshold_list, pixels_threshold=20, area_threshold=20, merge=True)
    for blob in blobs:
        blob_stats.append((blob.x(), blob.y(), compute(img, blob.rect())))

    img.to_rainbow(color_palette=sensor.PALETTE_IRONBOW)  # color it
    img.save(filepath+'/rainbow/'+tmp_name+'.jpg')

    for blob in blobs:
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    for blob_stat in blob_stats:
        img.draw_string(blob_stat[0], blob_stat[1] -
                        10, "%.2f C" % blob_stat[2], mono_space=False)
    img.save(filepath+'/after_draw/'+tmp_name+'.jpg')

    print("FPS %f - Lepton Temp: %f C" %
          (clock.fps(), sensor.ioctl(sensor.IOCTL_LEPTON_GET_FPA_TEMPERATURE)))
    time.sleep_ms(200)
