#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 14 09:02:08 2019

@author: daniele
"""

#%% --------------------------------- IMPORT ---------------------------------
import cv2 as cv
import os
import numpy as np
import time
import gaussians as gauss
import randomPoints as rp

#%% ----------------------------- INITIALIZATION -----------------------------
DAY = 'day'
NIGHT = 'night'
ESC_KEY = 27
WHITE_PIXEL = 255
GREY_PIXEL = 127

source = './webcam/web/'
threshold = 70
backgroundRatio = 0.7
originals = []
backgrounds = []

#==============================================================================
# # HYPERPARAMETERS
#==============================================================================
frame_rate = 5
take_freq = 2
WEIGHT = 3
avg_pixels = gauss.initGaussian().tolist()

#%% ----------------------------------MAIN------------------------------------

originals,backgrounds,foregrounds,avg_pixels = backgroundSubtraction(source,
                   frame_rate,take_freq, avg_pixels)


#%% ------------------------- BACKGROUND SUBTRACTION -------------------------

####################################################################################
#
# originals,backgrounds backgroundSubtraction (path_webcam, frame_rate, take_freq, threshold, ratio)
#                         (eg: ./Webcam/web7)
#
# params: path_webcam ->  path of webcam folder
# params: frame_rate  ->  how many frames take
# params: take_freq   ->  how often takes frame for originals and backgrounds 
# params: avg_pixels  --> initialization average pixels
#
# return: originals   ->  frame of original video, used for measure the accuracy
# return: backgrounds ->  backgrounds detected
# return: foregrounds ->  foregrounds detected
#
####################################################################################

def backgroundSubtraction(source, frame_rate, take_freq, avg_pixels):
        
    videoPaths = []
    original_frames = []
    bg_frames = []
    fg_frames = []
    initialThreshold = 70
    initialRatio = 0.9

    gaussians, y_gaussians = gauss.overallGaussians(avg_pixels)
    gauss.plotDayNightGaussian(gaussians)
    learning_rate = gauss.generateLearningRateTrading(gaussians)
    gauss.plotLearningRate(learning_rate)
    threshold = gauss.generateThreshold(gaussians)
#    gauss.comparisonThresholdGaussians(gaussians, threshold)
#    gauss.comparisonLearningRateGaussians(gaussians, learning_rate)
    
    mog = cv.createBackgroundSubtractorMOG2()    
    mog.setVarThreshold(initialThreshold)
    mog.setBackgroundRatio(initialRatio)
    
    videoList = os.listdir(source)
    for video in videoList:
        pathVideo = '{}/{}'.format(source, video)
        videoPaths.append(pathVideo)
        
    index = 0
    videoPaths.sort()
    num_video = len(videoPaths)
   
    takeFlag = False;
    
    print('\n')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    print('|\t  START BACKGROUND SUBTRACTION\t\t|')
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    start_time = time.time()
    
#    num_video = 100
    
    #for all video
    while (index < num_video):
        
        cap = cv.VideoCapture(videoPaths[index])
        
        print('|  '+str(index+1)+'-  load video:   '+videoPaths[index]+'\t|')
        
        index += 1
        
        end = False
        frameCount = 0;
        
        
        if(index%take_freq==0):
            takeFlag = True;
        
        # start video
        while(end == False):
            ret, frame = cap.read()
            if(ret == False):
                end = True
            else:
                # frame
                if(frameCount%frame_rate==0):
                    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
#                    frames.append(gray)
                    
                    fg = mog.apply(gray)
                    bg = mog.getBackgroundImage()
                    
                    cv.imshow('Original video', gray) 
                    cv.imshow('Background detected', bg)
                    cv.imshow('Foreground detected', fg)                 
                    
                    k = cv.waitKey(30)
    
                    # Press ESC to terminate
                    # Press S to save background (useless, is done in automatic way)
                    
                    if(takeFlag == True):
                        takeFlag = False
                        original_frames.append(gray)
                        fg_frames.append(fg)
                        bg_frames.append(bg)
                        
                        
                    if(k == ESC_KEY):
                        break
                    
                 #end if   
            frameCount += 1
            
        cap.release()
        #end video
        
        avg_pixel = rp.computePixelIntensityAverage(gray)
        avg_pixels = weightedAppend(avg_pixel, avg_pixels)
        
        print("Avg Pixel computed: {}".format(avg_pixel))
        
#        if(len(fg_frames)>2):
#            prev_fg = fg_frames[len(fg_frames)-2]
#            act_fg = fg
#            bounds = updateTransitionValue(avg_pixel, 
#                                        bounds, prev_fg, act_fg)
        
        # UPDATING GAUSSIANS        
        new_learning_rate, new_gaussians = updateGaussians(avg_pixels, 
                                                           gaussians, learning_rate)
            
        # UPDATING BACKGROUND RATIO ---> (1 - LEANRING RATE)
        ratio = updateBackgroundRatio(avg_pixel, new_learning_rate)
        mog.setBackgroundRatio(ratio)
        
        # UPDATING THRESHOLD
        threshold_value = updateThreshold(avg_pixel, threshold)
        mog.setVarThreshold(threshold_value)
        
        gauss.GaussianComparison(gaussians, new_gaussians,
                                learning_rate, new_learning_rate, avg_pixel)
        
        endVideo_time = time.time()
        print("|\t Spent time up to now: {:.2f} sec".format(endVideo_time - start_time))                            
        
        if(k == ESC_KEY):
            break      

    cv.destroyAllWindows()
    #end videos    
    
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    print('|\t  END BACKGROUND SUBTRACTION\t\t|')
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')   
    
    return original_frames, bg_frames, fg_frames, avg_pixels


# =============================================================================
#-----------------------------UPDATE AVERAGE PIXELS----------------------------
#    This function appends the new pixel average with a weight, in order to
#    have more consideration w.r.t. the initialization ones
#    
#    PARAMS:
#    - avg_pixel  --> new pixel average computed
#    - avg_pixels --> list of all pixel averages by time
#    
#    RETURN:
#    - avg_pixels --> the updated pixel average list 
# =============================================================================
def weightedAppend(avg_pixel, avg_pixels):
    
    w = WEIGHT    #Weight of the new avg_pixel wrt the init ones
    for i in range(0,w):    
        avg_pixels.append(avg_pixel)
    
    return avg_pixels

#==============================================================================
# --------------------------------UPDATE GAUSSIANS-----------------------------
#   
#    PARAMS:
#    - avg_pixels        --> list of all pixel averages by time
#    - old_gaussians     --> gaussians to be updated
#    - old_learning_rate --> learning rate to be updated
#    
#    RETURN:
#    - new_learning_rate --> updated learning rate 
#    - new_gaussians     --> updated gaussians
#
#==============================================================================    
def updateGaussians(avg_pixels, old_gaussians, old_learning_rate):  
    print("\n-----------START UPDATING GAUSSIANS-----------")   
    
    new_gaussians, new_y_gaussians = gauss.overallGaussians(avg_pixels)
    new_learning_rate = gauss.generateLearningRateTrading(new_gaussians)
    
#    gauss.GaussianComparison(old_gaussians, new_gaussians,
#                                old_learning_rate, new_learning_rate)
    
    print("\n-----------END UPDATING GAUSSIANS-----------")    
    
    return new_learning_rate, new_gaussians

#==============================================================================
#--------------------------UPDATE LEARNING RATE--------------------------------
#    
#   PARAMS:
#   - avg_pixel      --> new pixel average computed
#   - learning_rate  --> actual learning rate
#    
#   RETURN:
#   - ratio          --> updated background ratio
#  
#==============================================================================
def updateBackgroundRatio(avg_pixel, learning_rate):
    idx = intersection(learning_rate[DAY], learning_rate[NIGHT])
    
    # day time case
    if(avg_pixel >= idx):
      ratio = 1 - learning_rate[DAY][idx]
      
    # night time case
    else:
      ratio = learning_rate[NIGHT][idx]
    
    print('--Learning Rate : {}'.format(1 - ratio))
    return ratio
# =============================================================================
# ------------------------------UDPATE THRESHOLD-------------------------------
#    
#     PARAMS:
#     - avg_pixel  --> new pixel average computed
#     - threshol   --> threshold function
#  
#     RETURN:
#     - threshold_value  --> value of threshold when there is this avg_pixel
# =============================================================================
def updateThreshold(avg_pixel, threshold):
    
    threshold_value = threshold[avg_pixel]
    print('--Threshold: {}'.format(threshold_value))
    
    return threshold_value
  
# =============================================================================
# ---------------------------INTERSECTION--------------------------------------
#    Intersection between the function
#    
#    PARAMS:
#    - func1 --> function to be intersected
#    - func2 --> function to be intersected
#  
#    RETURN:
#    - IDX --> intersection point
#  
# =============================================================================
def intersection(func1, func2):
    idx = np.argwhere(np.diff(np.sign(func1 - func2)) != 0)
    idx = idx[0][0]
    
    return idx
# =============================================================================
# ------------------------------SHOW IMAGE-------------------------------------
# =============================================================================
def showImage(frame):
    
    while(True):
        cv.imshow("image", frame)
        
        k = cv.waitKey(30)
        if(k ==27):
            break
        
    cv.destroyAllWindows()


#%% Compute means

means = []
for frame in backgrounds:
    means.append(dynamicRatioEvaluation(frame))

#plt.hist(means, 50)

#==============================================================================
#%%
list_image = backgrounds
i = 0
cycle = True

while(cycle):
    
    cv.imshow('Backgroung GMM7', backgrounds[i])
    cv.imshow('Foregroung', foregrounds[i])
    cv.imshow('Original GMM7', originals[i])
#    cv.imshow('Dynamic Evaluation', drawAllRectangles(originals[i]))    


    print("Frame {}".format(i))    
    
    k = cv.waitKey(30)
    
    while(k != 97 and k != 115 and k != 27):
                k = cv.waitKey(30) & 0xff
        
                # key = s
                if(k == 115 and i < len(list_image)  - 1):
                        i = i + 1   # go to next frame
                        
                # key = a
                elif(k == 97 and i > 0):
                        i = i - 1   # go to previous frame
                        
                # key = ESC
                elif(k == 27):
                    print('Closing cv windows')
                    cv.destroyAllWindows()
                    cycle = False
                    break
    
cv.destroyAllWindows()
    
#%%


