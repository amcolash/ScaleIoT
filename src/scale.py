import cv2
import numpy as np
import os

useCamera = False


if (useCamera):
    # Camera 0 is the integrated web cam on my netbook
    camera_port = 0

    #Number of frames to throw away while the camera adjusts to light levels
    ramp_frames = 30

    # Init camera
    camera = cv2.VideoCapture(camera_port)

    def get_image():
     # read is the easiest way to get a full image out of a VideoCapture object.
     retval, im = camera.read()
     return im

    # Ramp the camera
    for i in xrange(ramp_frames):
     temp = get_image()
    print("Taking image...")
    # Take the actual image we want to keep
    cv2.imwrite('img/webcam.png', get_image())

    # Release the camera
    del(camera)

    filename = 'img/webcam.png'
else:
    filename = 'img/test.jpg'


image = cv2.imread(filename)

# Rotate the image
(h, w) = image.shape[:2]
center = (w / 2, h / 2)
M = cv2.getRotationMatrix2D(center, 180, 1.0)
image = cv2.warpAffine(image, M, (w, h))

# Find the screen in the image
upper = np.array([255, 255, 255])
lower = np.array([20, 10, 10])
mask1 = cv2.inRange(image, lower, upper)

# Get the masked portion
contours1 = cv2.findContours(mask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cnt = sorted(contours1[0], key = cv2.contourArea, reverse = True)[0]

# Crop to just the screen portion
x,y,w,h = cv2.boundingRect(cnt)
crop_img = image[y:y+h,x:x+w]

# Multiply image to make brighter
crop_img = cv2.cvtColor(crop_img,cv2.COLOR_BGR2GRAY)

# Get new mask and blur it
mask2 = cv2.inRange(crop_img, 0, 25)

# Crop edges because of artifacts
def is_contour_bad(c):
	area = cv2.contourArea(c)
	return area < 1200

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

# Write final image to be used in ssocr
cv2.imwrite('img/lcd_cropped.png', final)

# Use ssocr to figure out the value
output = os.popen('ssocr erosion -d -1 img/lcd_cropped.png').read()

# Fix output of extra '.' characters, add a '.' to end of value
output = output.replace('.', '')
output = output.replace('\n', '')
charlist = list(output)
charlist.insert(len(charlist) - 1, '.')
print ''.join(charlist)
