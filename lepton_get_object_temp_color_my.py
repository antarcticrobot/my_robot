# Lepton Get Object Temp Example
#
# This example shows off how to get an object's temperature using color tracking.

# By turning the AGC off and setting a max and min temperature range you can make the lepton into
# a great sensor for seeing objects of a particular temperature. That said, the FLIR lepton is a
# microblobometer and not a thermophile. So, it needs to re-calibrate itself often (which is called
# flat-field-correction - FFC). Additionally, microblobmeter devices require pprocessing support
# onboard to deal with the effects of temperature drift which is called radiometry support.

# FLIR Lepton Shutter Note: FLIR Leptons with radiometry and a shutter will pause the video often
# as they heatup to re-calibrate. This will happen less and less often as the sensor temperature
# stablizes. You can force the re-calibration to not happen if you need to via the lepton API.
# However, it is not recommended because the image will degrade overtime.

# If you are using a LEPTON other than the Lepton 3.5 this script may not work perfectly as other
# leptons don't have radiometry support or they don't activate their calibration process often
# enough to deal with temperature changes (FLIR 2.5).

import sensor, image, time, math,pyb,utime

# Color Tracking Thresholds (Grayscale Min, Grayscale Max)
#threshold_list = [(0, 255)]
#threshold_list = [(0, 128)]
threshold_list = [(200, 255)]

# Set the target temp range here
min_temp_in_celsius = -10.0
#max_temp_in_celsius = 0.0
#max_temp_in_celsius = 35.0
max_temp_in_celsius = 60.0

print("Resetting Lepton...")
# These settings are applied on reset
sensor.reset()
sensor.ioctl(sensor.IOCTL_LEPTON_SET_MEASUREMENT_MODE, True)
sensor.ioctl(sensor.IOCTL_LEPTON_SET_MEASUREMENT_RANGE, min_temp_in_celsius, max_temp_in_celsius)
print("Lepton Res (%dx%d)" % (sensor.ioctl(sensor.IOCTL_LEPTON_GET_WIDTH),
                              sensor.ioctl(sensor.IOCTL_LEPTON_GET_HEIGHT)))
print("Radiometry Available: " + ("Yes" if sensor.ioctl(sensor.IOCTL_LEPTON_GET_RADIOMETRY) else "No"))

sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=5000)
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

def map_g_to_temp(g):
    return ((g * (max_temp_in_celsius - min_temp_in_celsius)) / 255.0) + min_temp_in_celsius

def compute(img,rect):
    #m = img.get_statistics(thresholds=threshold_list,roi=rect).mean()
    m = img.get_statistics(roi=rect).mean()
    ans = map_g_to_temp(m)
    return ans

def get_time():
    now = pyb.millis()
    return now

width = sensor.ioctl(sensor.IOCTL_LEPTON_GET_WIDTH)
height = sensor.ioctl(sensor.IOCTL_LEPTON_GET_HEIGHT)
#filepath = "./2022_11_27_1800_tqyb18"
filepath = "."

if(True):
    clock.tick()
    img = sensor.snapshot()
    tmp_name=str(get_time())+".jpg"
    img.save("1.bmp")
    img.save("2.pgm")
    #img.save("test.ppm")
    img.save("3.jpg")
    img.save("4.jpeg")
    #img.save(filepath+'/raw/'+tmp_name)

    #print(img)
    #img2=image.Image('test.jpg', copy_to_fb=True)
    #img2=image.to_grayscale()
    #stream = image.ImageIO('./save_without_change.jpg','r')
    #img2 = stream.read(copy_to_fb=True, loop=True, pause=True)

    print(img)
    #print(img2)
    for i in range(0,10):
        print(str(img[i*160+i*10])+" "+str(map_g_to_temp(img[i*160+i*10])))
        #print(str(img2[i*160+60])+" "+str(map_g_to_temp(img2[i*160+60])))


    #blob_stats = []
    #blobs = img.find_blobs(threshold_list, pixels_threshold=20, area_threshold=20, merge=True)
    #for blob in blobs:
        #blob_stats.append((blob.x(), blob.y(), compute(img,blob.rect())))

    ##pieces = 10
    ##for i in range(pieces):
        ##tmp = [0,int(height/pieces*i),width,int(height/pieces)]
        ##print("horizontal i : %f"%(compute(img,tmp)))
        ##tmp = [int(width/pieces*i),0,int(width/pieces),height]
        ##print("vertival  : %f"%(compute(img,tmp)))


    #img.to_rainbow(color_palette=sensor.PALETTE_IRONBOW) # color it
    #img.save(filepath+'/rainbow/'+tmp_name)

    #for blob in blobs:
        #img.draw_rectangle(blob.rect())
        #img.draw_cross(blob.cx(), blob.cy())
    #for blob_stat in blob_stats:
        #img.draw_string(blob_stat[0], blob_stat[1] - 10, "%.2f C" % blob_stat[2], mono_space=False)
    #print("FPS %f - Lepton Temp: %f C" % (clock.fps(), sensor.ioctl(sensor.IOCTL_LEPTON_GET_FPA_TEMPERATURE)))
    #print("FPS %f - Lepton Temp: %f C" % (clock.fps(), sensor.ioctl(sensor.IOCTL_LEPTON_GET_AUX_TEMPERATURE)))
    #print(sensor.ioctl(sensor.IOCTL_LEPTON_GET_MEASUREMENT_RANGE))
    #img.save(filepath+'/after_draw/'+tmp_name)

    time.sleep_ms(500)
