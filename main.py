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
        dr = wool_rgb[i][0] - color[2]
        dg = wool_rgb[i][1] - color[1]
        db = wool_rgb[i][2] - color[0]
        color_distance = math.sqrt(dr*dr+dg*dg+db*db) 
        if color_distance < min_distance:
            min_distance = color_distance
            color_index = i 
    #print wool_name[color_index]
    return (wool_rgb[color_index][2], wool_rgb[color_index][1], wool_rgb[color_index][0])
    
def decide_wool_color_hsv(color):
    min_distance = 512 # larger than any other distance  
    for i in range(16):
        r = wool_rgb[i][0]
        g = wool_rgb[i][1]
        b = wool_rgb[i][2]
        point_rgb = np.zeros((1, 1, 3), np.uint8)
        point_rgb[0,0] = [b, g, r]
        point_hsv = cv2.cvtColor(point_rgb, cv2.COLOR_BGR2HSV)
        wool_hsv = point_hsv[0, 0] 
        dh = wool_hsv[0] - color[0]
        ds = wool_hsv[1] - color[1]
        dv = wool_hsv[2] - color[2]
        color_distance = math.sqrt(dh*dh+ds*ds+dv*dv) 
        if color_distance < min_distance:
            min_distance = color_distance
            color_index = i 
    #print wool_name[color_index]
    return (wool_rgb[color_index][2], wool_rgb[color_index][1], wool_rgb[color_index][0])
        
    

    

if __name__=="__main__":
    # read a image from a file 
    img = cv2.imread('test2.jpg')
    
    
    # resize
    height, width = img.shape[0:2]
    scale = math.sqrt(float(640 * 480) / (height * width))
    
    chunk_size = 40
    
    height = (int(height * scale / chunk_size) + 1) * chunk_size
    width = (int(width * scale / chunk_size) + 1) * chunk_size

    print "chunk_size =", chunk_size, "scalr =", scale
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_CUBIC)
    height, width = img.shape[0:2]
    #img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    
    row_num, col_num = img.shape[0:2]
    
    row_chunk_num = row_num / chunk_size
    col_chunk_num = col_num / chunk_size 
    
    # create a dst img
    #img2 = img
    img_mean_rgb = np.zeros((row_num, col_num, 3), np.uint8)
    img_mean_hsv = np.zeros((row_num, col_num, 3), np.uint8)
    img_wool = np.zeros((row_num, col_num, 3), np.uint8)
    img_wool_hsv = np.zeros((row_num, col_num, 3), np.uint8)
    
    
    for i in range(row_chunk_num):
        for j in range(col_chunk_num):
            #img_tmp_grey = cv2.cvtColor(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))]), cv2.COLOR_BGR2GRAY)
            img_tmp_hsv = cv2.cvtColor(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))], cv2.COLOR_BGR2HSV)
            mean_val = cv2.mean(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))])
            mean_val_hsv = cv2.mean(img_tmp_hsv)
            #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(img[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))])
            img_mean_rgb[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = mean_val[0:3]
            img_mean_hsv[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = mean_val_hsv[0:3]
            wool_color = decide_wool_color(mean_val[0:3])
            img_wool[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = wool_color
            wool_color = decide_wool_color_hsv(mean_val_hsv[0:3])
            img_wool_hsv[(chunk_size * i):(chunk_size * (i+1)), (chunk_size * j):(chunk_size * (j+1))] = wool_color
    img_mean_hsv = cv2.cvtColor(img_mean_hsv, cv2.COLOR_HSV2BGR)

            
    
    cv2.imshow('image1', img)
    cv2.imshow('image_mean_rgb', img_mean_rgb)
    cv2.imshow('image_mean_hsv', img_mean_hsv)
    cv2.imshow('image_wool', img_wool)
    cv2.imshow('image_wool_hsv', img_wool_hsv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #cv2.imwrite('chunked.jpg', img_wool)
    
