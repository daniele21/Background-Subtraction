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
import time
from scipy.stats import norm

#%% ----------------------------- INITIALIZATION -----------------------------

source = './webcam/web12/'
frame_rate = 5
take_freq = 2
threshold = 70
backgroundRatio = 0.7

originals = []
backgrounds = []

#init_means = summed_means
#means = init_means

originals,backgrounds,foregrounds,means = backgroundSubtraction(source,frame_rate,take_freq,threshold,backgroundRatio)

#%% ------------------------- BACKGROUND SUBTRACTION -------------------------

####################################################################################
#
# originals,backgrounds backgroundSubtraction (path_webcam, frame_rate, take_freq, threshold, ratio)
#                         (eg: ./Webcam/web7)
#
# params: path_webcam ->  path of webcam folder
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
    fg_frames = []
    means = []

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
            
        while(end == False):
            ret, frame = cap.read()
            if(ret == False):
                end = True
            else:
                if(frameCount%frame_rate==0):
                    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
#                    frames.append(gray)
                    
                    fg = mog.apply(gray)
                    bg = mog.getBackgroundImage()
                    
                    cv.imshow('Original video', gray) 
                    cv.imshow('Background detected', bg)
                    cv.imshow('Foreground detected', fg) 
                    #cv.imshow('Dynamic Evaluation', drawAllRectangles(gray))                    
                    
                    k = cv.waitKey(30)
    
                    # Press ESC to terminate
                    # Press S to save background (useless, is done in automatic way)
                    
                    if(takeFlag == True):
                        takeFlag = False
                        original_frames.append(gray)
                        fg_frames.append(fg)
                        bg_frames.append(bg)
                    
                    if(k == 27):
                        break
                    
                    if(k == 115):
                        bg_frames.append(bg)
                        fg_frames.append(fg)
                        original_frames.append(gray)
                    
            frameCount += 1
            
        cap.release()
           
        mean = dynamicRatioEvaluation(gray)
        means.append(mean)
        print(mean)        
        
        ratio, threshold = manage_bg_ratio(mean)
        mog.setBackgroundRatio(ratio)
        mog.setVarThreshold(threshold)        
        
        endVideo_time = time.time()
        print("|\t Spent time up to now: {:.2f} sec".format(endVideo_time - start_time))                            
        
        if(k == 27):
            break      

    cv.destroyAllWindows()
    
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    print('|\t\t\t\t\t\t|')
    print('|\t  END BACKGROUND SUBTRACTION\t\t|')
    print('|\t\t\t\t\t\t|')
    print('-------------------------------------------------')
    
#    daytimeDetection(means)    
    
    return original_frames, bg_frames, fg_frames, means

def manage_bg_ratio(mean):
    
    if(mean <= 65):
        ratio = 0.7
        threshold = 120
    elif(mean >= 105):
        ratio = 0.7
        threshold = 70
    else:
        ratio = 0.3
        threshold = 70
        
    print("Updating ratio to {}".format(ratio))
    return ratio, threshold

def dynamicRatioEvaluation(frame):
    points_value = []
    points_coord = []
    
    for i in range(1,100):
        
        row_left_up = int(np.random.uniform(30, 110))
        column_left_up= int(np.random.uniform(30, 110))
        points_coord.append([row_left_up, column_left_up])
        
        row_left_down = int(np.random.uniform(250, 330))
        column_left_down = int(np.random.uniform(30, 110))
        points_coord.append([row_left_down, column_left_down])        
        
        row_center = int(np.random.uniform(180-40, 180+40))
        column_center = int(np.random.uniform(320-40, 320+40))
        points_coord.append([row_center, column_center])
        
        row_right_up = int(np.random.uniform(30, 110))
        column_right_up= int(np.random.uniform(530, 610))
        points_coord.append([row_right_up, column_right_up])        
        
        row_right_down = int(np.random.uniform(250, 330))
        column_right_down= int(np.random.uniform(530, 610))
        points_coord.append([row_right_down, column_right_down])                       
        
        points_value.append(frame[row_center][column_center])
        points_value.append(frame[row_left_down][column_left_down])
        points_value.append(frame[row_left_up][column_left_up])
        points_value.append(frame[row_right_up][column_right_up])
        points_value.append(frame[row_right_down][column_right_down])
    
    
    drawPoints(frame, points_coord) 
    mean = int(np.mean(points_value))
#    print("Mean: " + str(mean))
    
    return mean

def daytimeDetection(means):
    day = []
    night = []    
    
    for mean in means:
        mid_point = int((max(means) - min(means))/2)
        split = mid_point + min(means)
        
        if(mean > split):        
            day.append(mean)
        elif(mean < split):
            night.append(mean)
            
    gauss_day = np.random.normal(int(np.mean(day)), np.std(day), 1000)
    plt.hist(gauss_day, color = 'green')
    gauss_night = np.random.normal(int(np.mean(night)), np.std(night), 1000)
    plt.hist(gauss_night, color = 'green')
    plt.show()
    plt.hist(means, 50, color = 'red', range = (40, 130))
    plt.show()

def drawPoints(frame, points):
    
#    temp = np.zeros((360,640,1))
    temp = np.copy(frame)
    
    for point in points:
        x = point[1]
        y = point[0]
        
        temp[y][x] = 255
        
#    showImage(temp)

def drawAllRectangles(frame):
    # Upper left
    temp = drawRectangle(frame, 30, 110, 30, 110)
    # Lower left 
    temp = drawRectangle(temp, 30, 110, 250, 330)
    # Upper right
    temp = drawRectangle(temp, 530, 610, 30, 110)
    # Lower right
    temp = drawRectangle(temp, 530, 610, 250, 330)
    # Center
    temp = drawRectangle(temp, 280, 360, 140, 220)
    
    return temp

def drawRectangle(frame, xA, xB, yA, yB):

    temp = np.copy(frame)
#    for i in range(yA, yB):   
    for j in range(xA, xB):
        temp[yA][j] = 255
        temp[yB][j] = 255
        
    for j in range(yA, yB):
        temp[j][xA] = 255
        temp[j][xB] = 255
        
    return temp;

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

plt.hist(means, 50)

#%% WEIGHTED GAUSSIAN UPDATE
#==============================================================================
# Weight factor
# w = 3
# 
# new_means = new_mean * w + np.mean(old_means) * len(old_means)
# 
#==============================================================================

def updateMeans(newMean):
    w = 3
    means.append(newMean * w)
    gauss_day, gauss_night = getGaussians()
#==============================================================================
#    -Get mean of the frame where foreground is detecting the transition time
#    -Use that mean to evaluate day/night probability
#    -Use this probability to check if the actual mean belongs to this probability range
#    -Update ratio and threshold
#==============================================================================
    
    
def generateDayNightGaussians(day, night):
    
    mu_day = int(np.mean(day))
    sigma_day = np.std(day)
    gauss_day = norm(mu_day, sigma_day)    

    mu_night = int(np.mean(night))
    sigma_night = np.std(night)
    gauss_night = norm(mu_night, sigma_night)
    
    x_axis = np.linspace(0,255,255)     #255 is the max luminosity    
    plt.xlim(10,150)
    
    y_day = gauss_day.pdf(x_axis)
    y_night = gauss_night.pdf(x_axis)

    plt.plot(x_axis, y_day, color = 'orange')
    plt.plot(x_axis, y_night, color = 'b')        
    plt.show()
    
    return y_day, y_night
 
def getGaussians():

    all_day = []
    all_night = []
    
    for mean in means:
        mid_point = int((max(means) - min(means))/2)
        split = mid_point + min(means)
        
        if(mean > split):        
            all_day.append(mean)
        elif(mean < split):
            all_night.append(mean)
            
    return generateDayNightGaussians(all_day, all_night)
#%% 
list_image = backgrounds
i = 0
cycle = True

while(cycle):
    
    cv.imshow('Backgroung', backgrounds[i])
    cv.imshow('Foregroung', foregrounds[i])
    cv.imshow('Original', originals[i])
#    cv.imshow('Dynamic Evaluation', drawAllRectangles(originals[i]))    
#    cv.moveWindow('Backgroung', 700,10)
#    cv.moveWindow('Foregroung', 0,380)
#    cv.moveWindow('Original', 0,5)

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
    
    