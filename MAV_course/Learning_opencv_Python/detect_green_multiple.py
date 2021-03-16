#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 15:40:07 2021

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

def find_continous_zeros(bin_array, thresh_lower, thresh_upper):
    start_index = []
    size = []
    
    count = 0
    
    flag_start = 0
    flag_zero = 0
    
    for i in range(len(bin_array)):
        
        if bin_array[i] == 0 and flag_start == 0:
            flag_start = 1
            start_index.append(i)
            count+=1
            if i == (len(bin_array) - 1):
                start_index.pop()
            if i == 0:
                start_index.pop()
                flag_zero = 1
                continue
            
        elif flag_start == 1 and bin_array[i] == 0:
            count+=1
            if i == (len(bin_array) - 1):
                if count <= thresh_upper:
                    size.append(count)
                else:
                    if len(start_index) > 0:
                        start_index.pop()        
            
        elif flag_start == 1 and bin_array[i] == 1:
            
            if thresh_lower <= count <= thresh_upper:
                size.append(count)
                flag_start = 0
                count = 0
                continue
            
            if len(start_index) > 0:
                start_index.pop()
                flag_start = 0
                count = 0
                
        
    if flag_zero == 1:
        if len(size) > 0:
            size.pop(0)
                
        
    return start_index, size


folder = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles_panels_mats/20190121-142935/'
savefolder = '/home/burhan/Desktop/MAV_course/Learning_opencv_Python/green_filtered_images/'

width = 520
height = 240
size = (width, height) #image dimensions

poles_images = load_images_from_folder(folder)

N = len(poles_images)

green_images = np.zeros((N, height, width))
green_bin_images = np.zeros((N, height, width))
green_contour_images = np.zeros((N, height, width, 3))


lower_green= np.array([65,75,65]) #BGR
upper_green = np.array([95,200,95])

#lower_green = np.array([50 ,0  ,  0]) #YUV
#upper_green = np.array([200,120,120])


for i in range(N):
    
    img = poles_images[i]
    
    green_mask = cv2.inRange(img, lower_green, upper_green)
    
    filtered_img = cv2.bitwise_and(img, img, mask = green_mask)
    
    filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(filtered_img, 75, 255, cv2.THRESH_BINARY) 
    
    #im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    
    #black_img = np.zeros((height, width, 3))
    
    #black_bin_img = np.zeros((height, width))
    
    #for item in range(len(contours)):
        #cnt = contours[item]
        #area = cv2.contourArea(cnt)
        #if area > 750:
            #cv2.drawContours(black_img, cnt, -1, (0,255,255), cv2.FILLED)
            #cv2.polylines(black_img, cnt, 1, (0,255,0), 1)
            #cv2.fillPoly(black_img, cnt, (255,255,255))
            
    
    #green_contour_images[i] = black_img
    
    green_bin_images[i] = thresh
    
    green_images[i] = filtered_img
    

THRESHOLD_LOW = 1
THRESHOLD_HIGH = 120

y_start = int((0.4)*height)

STEP = 5
    
for i in range(N):
    
    img = green_bin_images[i]/255.
    
    img[:y_start, :] = 0.
    
    for j in range(0,width,STEP):
        
        indeces, sizes = find_continous_zeros(img[y_start:,j], THRESHOLD_LOW, THRESHOLD_HIGH)
        
        for k in range(len(indeces)):
            
            img[y_start + indeces[k]:y_start + indeces[k] + sizes[k], j] = 1.
            
        img[y_start:, j:j+STEP] = np.tile(img[y_start:, j:j+1], (1,STEP))

        
    green_bin_images[i] = img*255.
    print(i)
        
        
    
for i in range(N):
    cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([green_images[i], green_bin_images[i]]))
    #cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([green_contour_images[i], poles_images[i]]))
    
