#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 13 19:20:43 2021

@author: burhan
"""

def find_continous_zeros(bin_array, thresh_lower, thresh_upper):
    
    ''' This function finds sequences of zeros in a binary array which have a length 
    in between (inclusive) thresh_lower and thresh_upper'''
    
    
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


def find_continous_ones(bin_array, thresh_lower, thresh_upper):
    
    ''' This function finds sequences of ones in a binary array which have a length 
    in between (inclusive) thresh_lower and thresh_upper'''
    
    
    start_index = []
    size = []
    
    count = 0
    
    flag_start = 0
    flag_zero = 0
    
    for i in range(len(bin_array)):
        
        if bin_array[i] == 1 and flag_start == 0:
            flag_start = 1
            start_index.append(i)
            count+=1
            if i == (len(bin_array) - 1):
                start_index.pop()
            #if i == 0:
            #    start_index.pop()
            #    flag_zero = 1
            #    continue
            
        elif flag_start == 1 and bin_array[i] == 1:
            count+=1
            if i == (len(bin_array) - 1):
                if count <= thresh_upper:
                    size.append(count)
                else:
                    if len(start_index) > 0:
                        start_index.pop()        
            
        elif flag_start == 1 and bin_array[i] == 0:
            
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