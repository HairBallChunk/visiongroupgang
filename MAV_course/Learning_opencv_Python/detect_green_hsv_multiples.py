#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 14:07:25 2021

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


folder = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles_panels_mats/20190121-142935/'
savefolder = '/home/burhan/Desktop/MAV_course/Learning_opencv_Python/green_hsv_filtered_images/'

width = 520
height = 240
size = (width, height) #image dimensions

area_threshold = 0.005
area_image = width*height

original_images = load_images_from_folder(folder)

N = len(original_images)

green_images = np.zeros((N, height, width, 3))



#lower_green= np.array([60,75,60]) #BGR
#upper_green = np.array([100,200,100])

#lower_green = np.array([50 ,0  ,  0]) #YUV
#upper_green = np.array([200,120,120])

lower_green= np.array([30,0,0]) #HSV
upper_green = np.array([90,255,255])

for i in range(N):
    
    img = original_images[i]
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    green_mask = cv2.inRange(img, lower_green, upper_green)
    
    filtered_img = cv2.bitwise_and(img, img, mask = green_mask)
    
    filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_HSV2BGR)
    
    green_images[i] = filtered_img
    
#for i in range(N):
#    
#    img = green_images[i]
#    img = img = img.astype('float32') #Data type conversion to keep opencv happy
#    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    
#    ret, thresh = cv2.threshold(img, 50, 255, 0) 
#    
#    thresh = thresh = thresh.astype('uint8') #Data type conversion to keep opencv happy
#    
#    im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
#    
#    print("i = ", i)
#    for item in range(len(contours)):
#        cnt = contours[item]
#        #area = cv2.contourArea(cnt)
#        #area_frac = area/area_image
#        if len(cnt) > 250:
#            #print("length is ", len(cnt), "area is ", area)
##            M = cv2.moments(cnt)
##            cx = int(M['m10']/M['m00'])
##            cy = int(M['m01']/M['m00'])
#            #x,y,w,h = cv2.boundingRect(cnt)
#            cv2.drawContours(green_images[i], cnt, -1, (0,255,0),2)
#            #cv2.imshow('image',og_image)
#            #cv2.waitKey(0)
#            #cv2.destroyAllWindows()
    

    

#for i in range(N):
    cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([original_images[i], green_images[i]]))
    
