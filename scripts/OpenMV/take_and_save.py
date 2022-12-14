# Snapshot Example
#
# Note: You will need an SD card to run this example.
#
# You can use your OpenMV Cam to save image files.

import sensor, image, pyb
#from pyb import UART

def get_time():
    now = pyb.millis()
    return now

#def send_uart():
    #uart = UART(3, 9600)
    #uart.write('hello')
    #uart.read(5) # read up to 5 bytes

#send_uart()


RED_LED_PIN = 1
BLUE_LED_PIN = 3

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
pyb.LED(BLUE_LED_PIN).on()

print("You're on camera!")
sensor.snapshot().save("example_ide_"+str(get_time())+".jpg") # or "example.bmp" (or others)


pyb.LED(BLUE_LED_PIN).off()
print("Done! Reset the camera to see the saved image.")
