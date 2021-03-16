#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 00:44:40 2021

@author: burhan
"""

import cv2
import os
import numpy as np
import natsort
import time
from binary_array_search import find_continous_ones, find_continous_zeros
from matplotlib import pyplot as plt

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
upper_green = np.array([90,150,90]) # 95,200,95

#parameters for poles and mats detection
THRESHOLD_LOW = 0
THRESHOLD_HIGH = 120

THRESHOLD_LOW_ONES = 2
THRESHOLD_HIGH_ONES = 35

y_start = int((0.5)*height)

STEP = 10

SECTION_SIZE = int(STEP*4)

SECTIONS = int(width/SECTION_SIZE) #(520/STEP)/4
#Each image section is 40 pixels wide

n_runs = 1

t_array = np.zeros(n_runs)

for t in range(n_runs):
    
    start_time = time.time()
    
    for i in range(N):
        
        img = poles_images[i]
        
        green_mask = cv2.inRange(img, lower_green, upper_green)
        
        filtered_img = cv2.bitwise_and(img, img, mask = green_mask)
        
        filtered_img = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2GRAY)
        
        ret, thresh = cv2.threshold(filtered_img, 70, 255, cv2.THRESH_BINARY)
        
        #green_bin_images[i] = thresh
        
        green_grey_3ch[i] = cv2.cvtColor(filtered_img, cv2.COLOR_GRAY2BGR)
        
        thresh = thresh/255. #converting to 255s and ones
        
        thresh[:y_start, :] = 0.
        
        for j in range(0,width,STEP):
            
            indeces, sizes = find_continous_zeros(thresh[y_start:,j], THRESHOLD_LOW, THRESHOLD_HIGH)
            
            for k in range(len(indeces)):
                
                thresh[y_start + indeces[k]:y_start + indeces[k] + sizes[k], j] = 1.
                
            thresh[y_start:, j:j+STEP] = np.tile(thresh[y_start:, j:j+1], (1,STEP))
            
        for r in range(y_start, height, STEP):
            
            indeces, sizes = find_continous_ones(thresh[r,:], THRESHOLD_LOW_ONES, THRESHOLD_HIGH_ONES)
            
            for k in range(len(indeces)):
                
                thresh[r, indeces[k]:indeces[k] + sizes[k]] = 0
                
            thresh[r:r+STEP, :] = np.tile(thresh[r:r+1, :], (STEP, 1))
            
        #pixel_percent_section = np.zeros(SECTIONS)
        
        thresh = thresh*255
            
        thresh = thresh = thresh.astype('uint8')
        
        green_bin_3ch[i] = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)
        
        cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([poles_images[i], green_grey_3ch[i], green_bin_3ch[i]]))
        
        #print(i)
        
    t_total = time.time() - start_time
    t_image = t_total/N
    
    t_array[t] = t_image
    
    print(t)
    
    
plt.plot(t_array)
    