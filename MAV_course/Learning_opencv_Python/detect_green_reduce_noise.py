#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:20:28 2021

@author: burhan
"""

import cv2
import os
import numpy as np
import natsort
import time
from binary_array_search import find_continous_ones, find_continous_zeros

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
#folder = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles/20190121-135009/'
savefolder = '/home/burhan/Desktop/MAV_course/Learning_opencv_Python/green_filtered_images/'

width = 520
height = 240
size = (width, height) #image dimensions

poles_images = load_images_from_folder(folder)

N = len(poles_images)

#green_images = np.zeros((N, height, width))
green_bin_images = np.zeros((N, height, width))
#green_grey_images = np.zeros((N, height, width, 3))

green_grey_3ch = np.zeros((N, height, width, 3))
green_bin_3ch = np.zeros((N, height, width, 3))

lower_green= np.array([65,75,65]) #BGR 65,75,65
upper_green = np.array([95,150,95]) # 95,200,95

#parameters for poles and mats detection
THRESHOLD_LOW = 0
THRESHOLD_HIGH = 120

THRESHOLD_LOW_ONES = 2
THRESHOLD_HIGH_ONES = 35

y_start = int((0.5)*height)

STEP = 10

SECTION_SIZE = int(40)

SECTIONS = int(width/SECTION_SIZE) #(520/STEP)/4
#Each image section is 40 pixels wide

start_time = time.time()

for i in range(N):
    
    img = poles_images[i]
    
    green_mask = cv2.inRange(img, lower_green, upper_green)
    
    filtered_img = cv2.bitwise_and(img, img, mask = green_mask)
    
    filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
    
    ret, thresh = cv2.threshold(filtered_img, 70, 255, cv2.THRESH_BINARY)
    
    green_bin_images[i] = thresh
    
    #green_images[i] = filtered_img
    
    green_grey_3ch[i] = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
    
    
for i in range(N):
    
    img = green_bin_images[i]/255 #converting to zeros and ones
    
    img[:y_start, :] = 0.
    
    #Loop to detect mats and remove holes
    for j in range(0,width,STEP):
        
        indeces, sizes = find_continous_zeros(img[y_start:,j], THRESHOLD_LOW, THRESHOLD_HIGH)
        
        for k in range(len(indeces)):
            
            img[y_start + indeces[k]:y_start + indeces[k] + sizes[k], j] = 1.
            
        img[y_start:, j:j+STEP] = np.tile(img[y_start:, j:j+1], (1,STEP))
        
    #Loop to denoise x axis and remove the background
    for r in range(y_start, height, STEP):
        
        indeces, sizes = find_continous_ones(img[r,:], THRESHOLD_LOW_ONES, THRESHOLD_HIGH_ONES)
        
        for k in range(len(indeces)):
            
            img[r, indeces[k]:indeces[k] + sizes[k]] = 0
            
        img[r:r+STEP, :] = np.tile(img[r:r+1, :], (STEP, 1))
        
    pixel_percent_section = np.zeros(SECTIONS)
    
    img = 255*img
        
    for m in range(SECTIONS):
        
        section = img[y_start:, m*SECTION_SIZE:(m+1)*SECTION_SIZE]
        
        frac_white = round(np.count_nonzero(section)/(SECTION_SIZE*(height- y_start)), 1)
        
        pixel_percent_section[m] = frac_white
        
        text_cord = (m*SECTION_SIZE, 50)
        
        cv2.putText(img, str(frac_white), text_cord, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 255*frac_white, 2, cv2.LINE_AA)
        
    img = img = img.astype('uint8')
        
    #green_bin_images[i] = img 
    
    green_bin_3ch[i] = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
    #cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([green_images[i], green_bin_images[i]]))
    
    cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([poles_images[i], green_grey_3ch[i], green_bin_3ch[i]]))
    
    #print(i)
    
t_total = time.time() - start_time
t_image = t_total/N
    
print("Computation time: ", t_image, " seconds per image")
