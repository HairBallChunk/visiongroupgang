#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 17:42:32 2021

@author: burhan
"""

import numpy as np
import cv2

#path = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles_panels'

img = cv2.imread('image_pole.jpg', 1)
img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)

cv2.imshow('image_pole', img)
cv2.waitKey(0)
cv2.destroyAllWindows()