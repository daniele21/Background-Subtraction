# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 21:32:32 2019

@author: andre
"""

#%% --------------------------------- IMPORT ---------------------------------

import cv2 as cv
import os
from matplotlib import pyplot as plt
import numpy as np

#%% ----------------------------- INITIALIZATION -----------------------------

source = './webcam/web4'
frame_rate = 3
take_freq = 7
threshold = 40
backgroundRatio = 0.7

originals = []
backgrounds = []

originals,backgrounds = backgroundSubtraction(source,frame_rate,take_freq,threshold,backgroundRatio)

#%% ------------------------- BACKGROUND SUBTRACTION -------------------------

####################################################################################
#
# originals,backgrounds backgroundSubtraction (path_webcam, frame_rate, take_freq, threshold, ratio)
#
# params: path_webcam ->  path of webcam folder
#                         (eg: ./Webcam/web7)
# params: frame_rate  ->  how many frames take
# params: take_freq   ->  how often takes frame for originals and backgrounds 
# params: threshold   ->  threshold for mog2
# params: ratio       ->  background ratio for mog2
#
# return: originals   ->  frame of original video, used for measure the accuracy
# return: backgrounds ->  background detected
#
####################################################################################

def backgroundSubtraction (source,frame_rate,take_freq,threshold,ratio):

    videoList = os.listdir(source)

    mog = cv.createBackgroundSubtractorMOG2()    
    mog.setVarThreshold(threshold)
    #mog.setHistory(5)
    mog.setBackgroundRatio(ratio)
    
    videoPaths = []
    
    original_frames = []
    bg_frames = []

    for video in videoList:
        pathVideo = '{}/{}'.format(source, video)
        videoPaths.append(pathVideo)
        
    index = 0
    videoPaths.sort
    num_video = len(videoPaths)
    
    takeFlag = False;
    
    print('\n')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    print('|\t  START BACKGROUND SUBTRACTION\t\t|')
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    
    #for all video
    while (index < num_video):
        
        cap = cv.VideoCapture(videoPaths[index])
        
        print('|  '+str(index+1)+'-  load video:   '+videoPaths[index]+'\t|')
        
        index += 1
        
        end = False
        frameCount = 0;
        
        frames = []
        
        if(index%take_freq==0):
            takeFlag = True;
            
        while(end == False):
            ret, frame = cap.read()
            if(ret == False):
                end = True
            else:
                if(frameCount%frame_rate==0):
                    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                    frames.append(gray)
            frameCount += 1
            
        cap.release()
        
        for frame in frames:
            
            fg = mog.apply(frame)
            bg = mog.getBackgroundImage()
            
            cv.imshow('Original video', frame) 
            cv.imshow('Background detected', bg)
            cv.imshow('Foreground detected', fg)
        
            k = cv.waitKey(30)
            
            # Press ESC to terminate
            # Press S to save background (useless, is done in automatic way)
            
            if(takeFlag == True):
                takeFlag = False
                original_frames.append(frame)
                bg_frames.append(bg)
            
            if(k == 27):
                break
            
            if(k == 115):
                bg_frames.append(bg)
                original_frames.append(frame)
            
        if(k == 27):
            break
            
    cv.destroyAllWindows()
    
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    print('|\t  END BACKGROUND SUBTRACTION\t\t|')
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    
    return original_frames,bg_frames
    
#%%
    
def process_frame(frame, mog):
   
    fg = mog.apply(frame)
    bg = mog.getBackgroundImage()
    
    cv.imshow('Original video', frame) 
    cv.imshow('Background detected', bg)
    cv.imshow('Foreground detected', fg)

    k = cv.waitKey(30)
    
    # Press ESC to terminate
    # Press S to save background (useless, is done in automatic way)
    
    if(takeFlag == True):
        takeFlag = False
        original_frames.append(frame)
        bg_frames.append(bg)
    
    if(k == 27):
        break
    
    if(k == 115):
        bg_frames.append(bg)
        original_frames.append(frame)