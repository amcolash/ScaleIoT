import cv2
import numpy as np
import os
import logging

STEPS=True
CAMERA=False

# Only show steps if the program is running by itself (not imported)
if __name__ != '__main__':
  STEPS=False

def get_image(cam):
  # read is the easiest way to get a full image out of a VideoCapture object.
  retval, im = cam.read()
  return im

def get_picture(use_camera):
  logger = logging.getLogger('scale.ocr')
  if (use_camera):
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0

    # Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 45

    # Init camera
    camera = cv2.VideoCapture(camera_port)

    # Ramp the camera
    logger.info("Taking image...")
    for i in xrange(ramp_frames):
      temp = get_image(camera)

    # Take the actual image we want to keep
    cv2.imwrite('img/webcam.png', get_image(camera))

    logger.info("Image Taken")

    # Release the camera
    del(camera)

    return 'img/webcam.png'
  else:
    return 'img/test1.png'

def ocr_image(image_name):
  logger = logging.getLogger('scale.ocr')
  logger.info("Start Image Processing")

  image = cv2.imread(image_name)

  if (STEPS):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Rotate the image
  (h, w) = image.shape[:2]
  center = (w / 2, h / 2)
  M = cv2.getRotationMatrix2D(center, 180, 1.0)
  image = cv2.warpAffine(image, M, (w, h))

  if (STEPS):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Find the screen in the image
  upper = np.array([255, 255, 255])
  lower = np.array([20, 10, 10])
  mask1 = cv2.inRange(image, lower, upper)

  if (STEPS):
    cv2.imshow('image',mask1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Get the masked portion
  contours1 = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  cnt = sorted(contours1[0], key = cv2.contourArea, reverse = True)[0]

  # Crop to just the screen portion
  x,y,w,h = cv2.boundingRect(cnt)
  crop_img = image[y:y+h,x+25:x+w]

  if (STEPS):
    cv2.imshow('image',crop_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Convert to grayscale
  crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)

  if (STEPS):
    cv2.imshow('image',crop_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Get new mask and blur it
  mask2 = cv2.inRange(crop_img, 0, 25)

  if (STEPS):
    cv2.imshow('image',mask2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Crop edges because of artifacts
  def is_contour_bad(c):
    area = cv2.contourArea(c)
    return area < 800

  mask3 = np.ones(mask2.shape[:2], dtype="uint8") * 255
  contours2 = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
  # loop over the contours
  for c in contours2[0]:
    # if the contour is bad, draw it on the mask
    if is_contour_bad(c):
      cv2.drawContours(mask3, [c], -1, 0, -1)

  # remove the contours from the image and show the resulting images
  final = cv2.bitwise_and(crop_img, crop_img, mask=mask3)
  # had to redo the range here, masking a mask didn't seem to work well
  final = cv2.inRange(final, 0, 25)

  # blur just a little bit
  final = cv2.blur(final, (2,2))

  if (STEPS):
    cv2.imshow('image',final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

  # Write final image to be used in ssocr
  cv2.imwrite('img/lcd_cropped.png', final)

  logger.info("End Image Processing")
  logger.info("Start OCR")

  # Use ssocr to figure out the value
  output = os.popen('ssocr erosion -d -1 img/lcd_cropped.png').read()

  # Fix output of extra '.' characters, add a '.' to end of value
  output = output.replace('.', '')
  output = output.replace('\n', '')
  charlist = list(output)
  charlist.insert(len(charlist) - 1, '.')
  weight = ''.join(charlist)

  logger.info("End OCR")

  return weight

def main():
  print ocr_image(get_picture(CAMERA))
  return

# Only run main if not imported
if __name__ == '__main__':
  main()
