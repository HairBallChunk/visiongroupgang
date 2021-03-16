# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:29:55 2021

@author: nora2
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

#image = cv2.imread('C:\\Users\\nora2\\Downloads\\cyberzoo_poles\\20190121-135009\\98377949.jpg')


directory = '/home/burhan/Desktop/MAV_course/AE4317_2019_datasets/cyberzoo_poles/20190121-135009/'
#savefolder = 'C:\\Users\\nora2\\Downloads\\cyberzoo_poles\\filtered_images'

for filename in os.listdir(directory):
    print(filename)
    
    if filename.endswith(".jpg"):
        
        img = cv2.imread(directory + filename)
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        
        lower_green= np.array([65,75,65]) #BGR
        upper_green = np.array([100,200,95])
        
        green_mask = cv2.inRange(img, lower_green, upper_green)

        green_img = cv2.bitwise_and(img, img, mask = green_mask)
    
            # Set threshold level
        threshold_level =70
        
        
        # Find coordinates of all pixels below threshold
        coords_gray = np.column_stack(np.where(gray < threshold_level))
        
        #print(coords_gray)
        
        coords_green = np.column_stack(np.where(green_img))
        print("Green Coordinates without mat",coords_green)
        
        
        # Create mask of all pixels lower than threshold level
        mask_gray = gray < threshold_level
        
         
        
        # Color the pixels in the mask
        gray_blue= img[mask_gray] = (204, 119, 0) #blue
        
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        
        cv2.waitKey(0)
       
        
        combined_mask = cv2.addWeighted(green_img, 0.9,img,0.5,0)
        
        #fly_coordinates
        
        cv2.imshow('image', np.hstack([green_img, img, combined_mask]))

                    
    else:
        print("no pictures found")
cv2.destroyAllWindows()