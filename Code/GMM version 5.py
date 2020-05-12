# -*- coding: utf-8 -*-
"""
@author: daniele
Created on Sat Apr 20 21:32:32 2019

@author: andre
"""

#%% --------------------------------- IMPORT ---------------------------------
import cv2 as cv
import os
from matplotlib import pyplot as plt
import numpy as np
import time
import randomPoints as rp
#%% ----------------------------- INITIALIZATION -----------------------------

source = './webcam/web_sunrise/'
frame_rate = 5
take_freq = 2
threshold = 70
backgroundRatio = 0.9

originals = []
backgrounds = []
APIs = []
bg_APIs = []

originals,backgrounds,foregrounds,means = backgroundSubtraction(source,frame_rate,take_freq,
                                                                threshold,
                                                                backgroundRatio,
                                                                APIs, bg_APIs)


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
#ackgroundRatio)
####################################################################################

def backgroundSubtraction (source,frame_rate,take_freq,threshold,ratio,APIs, bg_APIs):

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
           
        avg_pixel = rp.computePixelIntensityAverage(gray)
        APIs.append(avg_pixel)
        bg_APIs.append(rp.computePixelIntensityAverage(bg))
        
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


#%%
list_image = backgrounds
i = 0
cycle = True

while(cycle):
    
    cv.imshow('Backgroung GMM', backgrounds[i])
#    cv.imshow('Foregroung', foregrounds[i])
    cv.imshow('Original GMM', originals[i])
#    cv.imshow('Dynamic Evaluation', drawAllRectangles(originals[i]))    


    print("____________")
    print("Frame {}".format(i))
    print("API = {}".format(APIs[i*2]))
    print("bg_APIs = {}".format(bg_APIs[i*2]))
    
    k = cv.waitKey(30)
    
    while(k != 97 and k != 115 and k != 27):
                k = cv.waitKey(30) & 0xff
        
                # key = s
                if(k == 115 and i < len(list_image)  - 1):
                        i = i + 1   # go to next frame
                        
                # key = a
                elif(k == 97 and i > 0):
                        i = i - 1   # go to previous frame
                        
                # key = ESCs
                elif(k == 27):
                    print('Closing cv windows')
                    cv.destroyAllWindows()
                    cycle = False
                    break
    
cv.destroyAllWindows()
   
#%%
#%%
plt.title('Backgroung APIs --> Red\nOriginal Frame APIs --> Blue')
plt.xlabel('# Frame')
plt.ylabel('API')
plt.plot(bg_APIs, color = 'r')
plt.plot(APIs, color = 'b')
plt.show()

plt.title('Original Frame APIs')
plt.xlabel('# Frame')
plt.ylabel('API')
plt.plot(APIs, color = 'b')
plt.show()

plt.title('Backgroung APIs')
plt.xlabel('# Frame')
plt.ylabel('API')
plt.plot(bg_APIs, color = 'r')
plt.show()
