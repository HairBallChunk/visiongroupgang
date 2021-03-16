#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:43:45 2021

@author: burhan
"""

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
        size.pop(0)
                
        
    return start_index, size


test_array = np.array([0,0,0,0,1,1,1,1,0,1,1,0,1,1,0,0,0,0,1,0,0,0,1,1,1,1,1,0])

indeces, sizes = find_continous_zeros(test_array, 2,7)


for k in range(len(indeces)):
            
    test_array[indeces[k]:indeces[k] + sizes[k]] = 1.
            
            
        