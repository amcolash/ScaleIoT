import ocr
import RPi.GPIO as GPIO
import time
import signal
import sys
import os
import logging

# LED GPIO Pin
GREEN_LED=12

# Trigger GPIO pin when scale LED activated
TRIGGER=16

def signal_handler(signal, frame):
  logging.getLogger('scale').info("SIGINT, closing safely")
  GPIO.cleanup()
  sys.exit(0)

def event_trigger(channel):
  logger = logging.getLogger('scale')
  logger.info("edge detect")
  time.sleep(3)
  GPIO.output(GREEN_LED, True)

  image = ocr.get_picture(True)
  weight = ocr.ocr_image(image)
  logger.info("weight: " + weight)

  GPIO.output(GREEN_LED, False)

def exception_handler(type, value, tb):
  logger = logging.getLogger('scale')
  logger.exception("Uncaught exception: {0}".format(str(value)))

def setup_logger():
  # Used from https://docs.python.org/2/howto/logging-cookbook.html
  # create logger
  logger = logging.getLogger('scale')
  logger.setLevel(logging.DEBUG)

  # create file handler which logs even debug messages
  fh = logging.FileHandler('log.txt')
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
  GPIO.setup(TRIGGER, GPIO.IN) # Set up input trigger pin

  # Reset LED
  GPIO.output(GREEN_LED, False)

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
