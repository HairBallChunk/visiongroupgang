#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 00:32:39 2021

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


green_bin_images = np.zeros((N, height, width, 3))


lower_green= np.array([65,75,65]) #BGR
upper_green = np.array([100,200,95])

n_runs = 1

t_array = np.zeros(n_runs)

for t in range(n_runs):
    
    start_time = time.time()

    for i in range(N):
        
        img = poles_images[i]
            
        green_mask = cv2.inRange(img, lower_green, upper_green)
    
        green_img = cv2.bitwise_and(img, img, mask = green_mask)
            
        ret,thresh = cv2.threshold(green_mask,128,255,cv2.THRESH_BINARY)
        
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
        coords_green = np.column_stack(np.where(green_img))
        
        for j,cnt in enumerate(contours):
        # if the contour has no other contours inside of it
        #print(cv2.contourArea(cnt))
            if cv2.contourArea(cnt) > 5000: 
                coord= cnt[:,0,:]
                sorted_coord= coord[coord[:,1].argsort()]
                #cv2.drawContours(green_img, contours[i], -1, (0,255,0),2)
                #print("Sorted",sorted_coord)
                unique_coord, idx = np.unique(sorted_coord[ : ,0], return_index=True)
                out = sorted_coord[idx] 
                # print("Unique",out)
                
                for point in out:
                    
                    x,y = point.ravel()
                    cv2.circle(green_img,(x,y),3,(255, 0, 0),2)
                    
                    
        green_bin_images[i] = green_img
                    
        cv2.imwrite(savefolder + str(i) + '.jpg', np.hstack([poles_images[i], green_bin_images[i]]))

       
    t_total = time.time() - start_time
    t_image = t_total/N
    
    t_array[t] = t_image
    
    print(t)
    
    
plt.plot(t_array)
