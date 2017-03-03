import ocr
import stats
import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import logging
import json

# Define MIN/MAX ranges for weight, if outside range error (I used +/- 10%)
MIN_WEIGHT=160
MAX_WEIGHT=220

# LED GPIO Pin
GREEN_LED=13
# LED GPIO Pin
RED_LED=19

# Trigger GPIO pin when scale LED activated
TRIGGER=26

def signal_handler(signal, frame):
  logging.getLogger('scale').info("SIGINT or SIGTERM, closing safely")
  GPIO.cleanup()
  sys.exit(0)

def event_trigger(channel):
  logger = logging.getLogger('scale')
  logger.info("Edge Detect")
  time.sleep(3)
  GPIO.output(GREEN_LED, True)

  # Take picture with webcam
  image = ocr.get_picture(True)
  # Turn off LED when done
  GPIO.output(GREEN_LED, False)

  # OCR the image
  weight = ocr.ocr_image(image)

  # Live on the wild side, exceptions are handled globally for us (probably bad)
  weight = float(weight)

  if (weight < MIN_WEIGHT) or (weight > MAX_WEIGHT):
    raise ValueError('Invalid Weight!')
  else:
    logger.info("Weight: " + str(weight))

    # Open the json file
    with open('../web/data.json') as f:
      data = json.load(f)

    # Get time/date
    # timestamp = time.strftime('%x %X %Z')
    timestamp = int(round(time.time() * 1000))

    # Append to the temp json object
    data.update({timestamp : weight})

    # Write changes to the file
    with open('../web/data.json', 'w') as f:
      json.dump(data, f, sort_keys=True, indent=2)

    # Update stats
    stats.get_stats()

    # Flash Green LED for successful weight capture
    for i in range(0,6):
      GPIO.output(GREEN_LED, True)
      time.sleep(0.35)
      GPIO.output(GREEN_LED, False)
      time.sleep(0.35)


def exception_handler(type, value, tb):
  logger = logging.getLogger('scale')
  logger.exception("Uncaught exception: {0}".format(str(value)))

  # Blink Red LED on exceptions
  for i in range(0,6):
    GPIO.output(RED_LED, True)
    time.sleep(0.35)
    GPIO.output(RED_LED, False)
    time.sleep(0.35)

def setup_logger():
  # Used from https://docs.python.org/2/howto/logging-cookbook.html
  # create logger
  logger = logging.getLogger('scale')
  logger.setLevel(logging.DEBUG)

  # create file handler which logs even debug messages
  fh = logging.FileHandler('log.txt', mode='w')
  fh.setLevel(logging.DEBUG)

  # create console handler with a higher log level
  ch = logging.StreamHandler()
  ch.setLevel(logging.DEBUG)

  # create formatter and add it to the handlers
  formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
  fh.setFormatter(formatter)
  ch.setFormatter(formatter)

  # add the handlers to the logger
  logger.addHandler(fh)
  logger.addHandler(ch)

  # Install exception handler
  sys.excepthook = exception_handler

def setup_gpio():
  # Set up pins
  GPIO.setwarnings(False) # Remove the annoying warnings, nothing else is using the pins
  GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme

  GPIO.setup(GREEN_LED, GPIO.OUT) # Green LED pin set as output
  GPIO.setup(RED_LED, GPIO.OUT) # Red LED pin set as output

  GPIO.setup(TRIGGER, GPIO.IN) # Set up input trigger pin

  # Reset LED
  GPIO.output(GREEN_LED, False)
  GPIO.output(RED_LED, False)

  # Set up trigger event handler
  GPIO.add_event_detect(TRIGGER, GPIO.FALLING, callback=event_trigger, bouncetime=300)

  # Set up SIGINT and SIGTERM event handlers (cleanly exit after ctrl-c and kill)
  signal.signal(signal.SIGINT, signal_handler)
  signal.signal(signal.SIGTERM, signal_handler)


def main():
  setup_logger()
  setup_gpio()

  logger = logging.getLogger('scale')

  # Print where this thing is running from
  logger.info("starting scaleiot, current directory: " + os.getcwd())

  while True:
    time.sleep(30)

  GPIO.cleanup()       # clean up GPIO


if __name__ == '__main__':
  main()
