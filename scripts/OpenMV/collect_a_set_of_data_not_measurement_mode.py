
import sensor
import image
import time
import pyb
import utime

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
threshold_list = [( 0, 100,  -128,   127,   -128,  127)]

print("Resetting Lepton...")
# These settings are applied on reset
sensor.reset()
print("Lepton Res (%dx%d)" % (sensor.ioctl(sensor.IOCTL_LEPTON_GET_WIDTH),
                              sensor.ioctl(sensor.IOCTL_LEPTON_GET_HEIGHT)))
print("Radiometry Available: " + ("Yes" if sensor.ioctl(sensor.IOCTL_LEPTON_GET_RADIOMETRY) else "No"))
# Make the color palette cool
sensor.set_color_palette(sensor.PALETTE_IRONBOW)

sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=5000)
clock = time.clock()


def get_time():
    now = pyb.millis()
    return now


filepath = "./2023_02_20_1620_pyg"
#filepath = "."


def save_as_four_format(fileName):
    img.save(fileName+".bmp")
    #img.save(fileName+".pgm")
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
    #for blob in blobs:
        #blob_stats.append((blob.x(), blob.y(), compute(img, blob.rect())))

    #img.to_rainbow(color_palette=sensor.PALETTE_IRONBOW)  # color it
    img.save(filepath+'/rainbow/'+tmp_name+'.jpg')

    for blob in blobs:
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    #for blob_stat in blob_stats:
        #img.draw_string(blob_stat[0], blob_stat[1] -
                        #10, "%.2f C" % blob_stat[2], mono_space=False)
    img.save(filepath+'/after_draw/'+tmp_name+'.jpg')

    print("FPS %f - Lepton Temp: %f C" %
          (clock.fps(), sensor.ioctl(sensor.IOCTL_LEPTON_GET_FPA_TEMPERATURE)))
    time.sleep_ms(200)
