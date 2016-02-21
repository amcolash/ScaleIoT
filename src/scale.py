import scale_ocr
import RPi.GPIO as GPIO
import time
import signal

# LED GPIO Pin
LED=12

# Trigger GPIO pin when scale LED activated
TRIGGER=16

# Set up pins
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(LED, GPIO.OUT) # LED pin set as output
GPIO.setup(TRIGGER, GPIO.IN) # Set up input trigger pin

def event_trigger(channel):
  print "edge detect"

GPIO.add_event_detect(17, GPIO.FALLING, callback=event_trigger, bouncetime=300)

try:
  while 1:
    time.sleep(forever)
except KeyboardInterrupt:
  GPIO.cleanup() # clean up with CTRL+C exit

GPIO.cleanup()       # clean up GPIO on normal exit
