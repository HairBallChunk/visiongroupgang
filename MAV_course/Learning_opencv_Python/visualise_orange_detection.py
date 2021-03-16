#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 6 21:52:45 2021

@author: burhan
"""

import cv2
import os
import numpy as np
import natsort

def load_images_from_folder(folder):
    images = []
    files = os.listdir(folder)
    files = natsort.natsorted(files)
    for filename in files:
        img = cv2.imread(os.path.join(folder,filename), 1)
        if img is not None:
            images.append(img)
    return images

folder_name = 'green_filtered_images/'

retreive_path = '/home/burhan/Desktop/MAV_course/Learning_opencv_Python/' + folder_name

comparision_images = load_images_from_folder(retreive_path)

for i in range(len(comparision_images)):
    cv2.imshow('image_pole', comparision_images[i])
    cv2.waitKey(0)

cv2.destroyAllWindows()

