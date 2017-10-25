# USAGE
# python skindetector.py

# import the necessary packages
from pyimagesearch import imutils
import numpy as np
import argparse
import cv2


# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

image_dir = "./images/test_image" 
numpy_file = "./images/test_image_np"

for i in range(1,7):
	img = image_dir + str(i) + '.jpg'
	frame = cv2.imread(img)

	# resize the frame, convert it to the HSV color space,
	# and determine the HSV pixel intensities that fall into
	# the speicifed upper and lower boundaries
	frame = imutils.resize(frame, width = 400) 
	converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	skinMask = cv2.inRange(converted, lower, upper)

	# apply a series of erosions and dilations to the mask
	# using an elliptical kernel
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	skinMask = cv2.erode(skinMask, kernel, iterations = 2)
	skinMask = cv2.dilate(skinMask, kernel, iterations = 2)

	# blur the mask to help remove noise, then apply the
	# mask to the frame
	skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
	skin = cv2.bitwise_and(frame, frame, mask = skinMask)

	nfile = numpy_file + str(i)

	print img
	print nfile

	np.save(nfile, skin)

	# show the skin in the image along with the mask
	cv2.imshow("images", np.hstack([frame, skin]))
	#cv2.imshow("images", skin)
	cv2.waitKey()
