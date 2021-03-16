#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 12:18:07 2021

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
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        if img is not None:
            images.append(img)
    return images


folder = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles/20190121-135009/'
savefolder = '/home/burhan/Desktop/MAV_course/Learning_opencv_Python/orange_poles_yuv_filtered/'

width = 520
height = 240
size = (width, height) #image dimensions

area_threshold = 0.005


poles_images = load_images_from_folder(folder)

N = len(poles_images)

orange_images = np.zeros((N, height, width, 3))

lower_orange = np.array([70,0,160]) #YUV
upper_orange = np.array([200,120,220])


lower_green = np.array([50 ,0  ,  0]) #YUV
upper_green = np.array([200,120,120])


for i in range(N):
    
    img = poles_images[i]
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    
    orange_mask = cv2.inRange(img, lower_orange, upper_orange)
    
    filtered_img = cv2.bitwise_and(img, img, mask = orange_mask)
    
    filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_YUV2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_YUV2BGR)
    
    orange_images[i] = filtered_img
    
#    sbs = np.zeros((height, 2*width, 3), np.uint8)
#    
#    sbs[:height, :width, :3] = img
#    sbs[:height, width:2*width, :3] = orange_img
#    
#    compare_images[i] = sbs
    
find_contours = np.copy(orange_images)

for i in range(N):
    
    img = find_contours[i]
    img = img = img.astype('float32')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    og_image = orange_images[i]
    
    ret, thresh = cv2.threshold(img, 100, 255, 0)
    
    thresh = thresh = thresh.astype('uint8')
    
    im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    
    print("i = ", i)
    for item in range(len(contours)):
        cnt = contours[item]
        area = cv2.contourArea(cnt)
        area_frac = area/(520*240)
        if len(cnt) > 100 or area_frac > area_threshold:
            #print("length is ", len(cnt), "area is ", area)
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(og_image,(x,y),(x+w,y+h),(0,255,0),2)
            #cv2.imshow('image',og_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
    orange_images[i] = og_image
    
    

for i in range(N):
    cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([poles_images[i], orange_images[i]]))
    
