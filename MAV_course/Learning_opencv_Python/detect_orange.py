#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 18:17:11 2021

@author: burhan
"""


import numpy as np
import cv2

#path = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles_panels'

img = cv2.imread('image_pole.jpg',1)
img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

lower_orange = np.array([0,0,130]) #BGR
upper_orange = np.array([100,100,255])

orange_mask = cv2.inRange(img, lower_orange, upper_orange)

orange_img = cv2.bitwise_and(img, img, mask = orange_mask)

cv2.imshow('image_pole', np.hstack([orange_img, img]))
cv2.waitKey(0)
cv2.destroyAllWindows()