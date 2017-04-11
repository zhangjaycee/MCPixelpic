#!/usr/bin/python
#coding: utf-8

import numpy as np
import cv2
import math

wool_rgb = [ (221,221,221), (219,125,62), (179,80,188), (107,138,201), (177,166,39), (65,174,56), (208,132,153), (64,64,64), (154,161,161), (46,110,137), (126,61,181), (46,56,141), (79,50,31), (53,70,27), (150,52,48), (25,22,22) ]
wool_name = ["white", "orange", "magenta", "lightBlue", "yellow", "lime", "pink", "gray", "silver", "cyan", "purple", "blue" ,"brown", "green", "red", "black"]

def decide_wool_color(color):
    min_distance = 512 # larger than any other distance  
    for i in range(16):
        b = wool_rgb[i][0] - color[2]
        g = wool_rgb[i][1] - color[1]
        r = wool_rgb[i][2] - color[0]
        color_distance = math.sqrt(r*r+g*g+b*b) 
        if color_distance < min_distance:
            min_distance = color_distance
            color_index = i 
    #print wool_name[color_index]
    return (wool_rgb[color_index][2], wool_rgb[color_index][1], wool_rgb[color_index][0])
    
    

if __name__=="__main__":
    # read a image from a file 
    img = cv2.imread('test.jpg')
    
    
    # resize
    height, width = img.shape[0:2]
    print "--->", height, width
    scale = math.sqrt(float(640 * 480) / (height * width))
    
    chunk_size = 30
    
    height = (int(height * scale / chunk_size) + 1) * chunk_size
    width = (int(width * scale / chunk_size) + 1) * chunk_size

    print "scalr =", scale
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    height, width = img.shape[0:2]
    print "--->", height, width
    #img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    row_num, col_num = img.shape[0:2]
    
    row_chunk_num = row_num / chunk_size
    col_chunk_num = col_num / chunk_size 
    
    # create a dst img
    #img2 = img
    img2 = np.zeros((row_num, col_num, 3), np.uint8)
    img_wool = np.zeros((row_num, col_num, 3), np.uint8)
    
    
    for i in range(row_chunk_num):
        for j in range(col_chunk_num):
            mean_val = cv2.mean(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))])
            img2[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = mean_val[0:3]
            wool_color = decide_wool_color(mean_val[0:3])
            img_wool[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = wool_color
            
    '''
    for i in range(row_chunk_num):
        mean_val = cv2.mean(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * col_chunk_num):col_num])
        img2[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * col_chunk_num):col_num] = mean_val[0:3]
    
    
    for j in range(col_chunk_num):
        mean_val = cv2.mean(img[(chunk_size * row_chunk_num):row_num, (chunk_size * j):(chunk_size * (j+1))])
        img2[(chunk_size * row_chunk_num):row_num, (chunk_size * j):(chunk_size * (j+1))] = mean_val[0:3]
    
    mean_val = cv2.mean(img[(chunk_size * row_chunk_num):row_num, (chunk_size * col_chunk_num):col_num])
    img2[(chunk_size * row_chunk_num):row_num, (chunk_size * col_chunk_num):col_num] = mean_val[0:3]
    '''
    
    cv2.imshow('image1', img)
    cv2.imshow('image2', img2)
    cv2.imshow('image_wool', img_wool)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('chunked.jpg', img2)
    
    
    # show a img
    #cv2.imshow('image', img)
    #cv2.imshow('image_grey', img2)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
