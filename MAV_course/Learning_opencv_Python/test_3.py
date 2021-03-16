# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 17:22:49 2021

@author: nora2
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
import os

def takeSecond(elem):
    return elem[1]

image = cv2.imread('C:\\Users\\nora2\\Downloads\\cyberzoo_poles\\20190121-135009\\98377949.jpg')


directory = 'C:\\Users\\nora2\Downloads\\cyberzoo_poles\\20190121-135009'
savefolder = 'C:\\Users\\nora2\\Downloads\\cyberzoo_poles\\filtered_images\\'

for filename in os.listdir(directory):
    if filename.endswith(".jpg"):
        
        img = cv2.imread('C:\\Users\\nora2\\Downloads\\cyberzoo_poles\\20190121-135009\\'+filename)
        img = cv2.rotate(img, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        lower_green= np.array([65,75,65]) #BGR
        upper_green = np.array([100,200,95])
        
        green_mask = cv2.inRange(img, lower_green, upper_green)

        green_img = cv2.bitwise_and(img, img, mask = green_mask)
        

        ret,thresh = cv2.threshold(green_mask,128,255,cv2.THRESH_BINARY)
        

        contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        
        coords_green = np.column_stack(np.where(green_img))
        #print("Green Coordinates without mat",coords_green)
        
        # take second element for sort
        #find mats
        #for item in contours:
        for i,cnt in enumerate(contours):
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

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break    
        cv2.imshow('image', np.hstack([green_img]))
        cv2.imwrite(savefolder + str(filename), green_img)
                    
    else:
        print("no pictures found")
cv2.destroyAllWindows()


    