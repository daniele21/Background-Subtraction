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
DELTA_FG = 10000
OFFSET = 5
NORMAL_BG_RATIO = 0.9
RAPID_BG_RATIO = 0.1
NORMAL_THRESHOLD = 70
NIGHT_THRESHOLD = 130
# INIT VALUE
day_bound = 108
night_bound = 70
avg_pixels = gauss.initGaussian().tolist()
#==============================================================================
# 
#==============================================================================


bounds = {DAY:day_bound, NIGHT:night_bound}


#%% ----------------------------------MAIN------------------------------------
originals,backgrounds,foregrounds,avg_pixels = backgroundSubtraction(source,
                   frame_rate,take_freq, avg_pixels, bounds)

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

def backgroundSubtraction (source, frame_rate, take_freq, avg_pixels, bounds):

    threshold = 70
    ratio = 0.7

    videoList = os.listdir(source)

    mog = cv.createBackgroundSubtractorMOG2()    
    mog.setVarThreshold(threshold)
    #mog.setHistory(5)
    mog.setBackgroundRatio(ratio)
    
    videoPaths = []
    
    original_frames = []
    bg_frames = []
    fg_frames = []

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
                    #cv.imshow('Dynamic Evaluation', drawAllRectangles(gray))                    
                    
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
        #avg_pixels.append(avg_pixel)
        print("Avg Pixel computed: {}".format(avg_pixel))
        
        if(len(fg_frames)>2):
            prev_fg = fg_frames[len(fg_frames)-2]
            act_fg = fg
#            showImage(prev_fg)
#            showImage(act_fg)
            bounds = updateTransitionValue(avg_pixel, 
                                        bounds, prev_fg, act_fg)
                    
        ratio, threshold = manage_bg_ratio(avg_pixel, bounds)
        
        mog.setBackgroundRatio(ratio)
        mog.setVarThreshold(threshold)  
        
        bounds = updateGaussians(avg_pixel, avg_pixels, bounds)
        
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

#==============================================================================
# ----------------------UPDATE GAUSSIANS--------------------------------------
#   - update givind more weight to the new avg_pixel    X
#   - update giving weight and foregetting the old results (to be find)
#
#==============================================================================

def updateGaussians(avg_pixel, avg_pixels, bounds):
    
    print("\n-----------START UPDATING GAUSSIANS-----------")
    
    old_gaussians, old_y_gaussians = gauss.overallGaussians(avg_pixels)    
    probabilities = gauss.getProbabilities(bounds, old_gaussians)
     
    print("Probability of day bound --> {:.5f}".format(probabilities[DAY]))    
    print("Probability of night bound --> {:.5f}".format(probabilities[NIGHT]))    
    
#    gauss.plotDayNightGaussian(old_gauss_day, old_gauss_night, 'Old Gaussians')    
    
    w = WEIGHT    #Weight of the new avg_pixel wrt the init ones
    for i in range(0,w):    
        avg_pixels.append(avg_pixel)
    
    new_gaussians, new_y_gaussians = gauss.overallGaussians(avg_pixels)
    
#    gauss.plotDayNightGaussian(new_gauss_day, new_gauss_night, 'Updated Gaussians')   
    
    new_bounds = gauss.getPixelIntensities(probabilities, new_gaussians)
    
    gauss.plotGaussianComparison(old_gaussians, new_gaussians, bounds, new_bounds)
    
    print("New day bound fixed at    {}".format(new_bounds[DAY]))
    print("New night bound fixed at  {}".format(new_bounds[NIGHT]))
    
    print("\n-----------END UPDATING GAUSSIANS-----------")    
    
    return new_bounds

#==============================================================================
# 
#==============================================================================
def updateTransitionValue(avg_pixel, bounds, prev_fg, act_fg):
    # intensity difference of 127 and 255 intensity pixel between two consecutive foreground    
    diff = 0
    print("\n-----------START UPDATING TRANSITION VALUE-----------")
    # check if you are in a moment near the transition
    if(avg_pixel > bounds[NIGHT] - OFFSET and avg_pixel < bounds[DAY] + OFFSET):
        prev_fg_value = np.count_nonzero(prev_fg == WHITE_PIXEL) + np.count_nonzero(prev_fg == GREY_PIXEL)
        act_fg_value = np.count_nonzero(act_fg == WHITE_PIXEL) + np.count_nonzero(act_fg == GREY_PIXEL)
        diff = abs(act_fg_value - prev_fg_value)
        
#        showImage(prev_fg)
#        showImage(act_fg)

        if(diff > DELTA_FG):
            print("Delta Foreground Exceeded")
            # case in which you are 
            if(abs(avg_pixel - bounds[DAY]) > abs(avg_pixel - bounds[NIGHT])):
                bounds[NIGHT] = avg_pixel# error margin
            else:
                bounds[DAY] = avg_pixel
            
                print("New day bound fixed at    {}".format(bounds[DAY]))
                print("New night bound fixed at  {}".format(bounds[NIGHT]))
    

         
    print("\n-----------END UPDATING TRANSITION VALUE-----------")     
    
    return bounds

#diff = []
#for i in range(0,len(foregrounds)):
#    if(i>0):
#        actual = np.count_nonzero(foregrounds[i]==127) + np.count_nonzero(foregrounds[i]==255)
#        prev = np.count_nonzero(foregrounds[i-1]==127) + np.count_nonzero(foregrounds[i-1]==255)    
#        diff.append(abs(actual - prev))      
#==============================================================================
#         
#==============================================================================
def manage_bg_ratio(avg_pixel, bounds):
    
    day_label = ''    
    
    if(avg_pixel <= bounds[NIGHT]):
        day_label = 'Night_Time'        
        ratio = NORMAL_BG_RATIO
        threshold = NIGHT_THRESHOLD
    elif(avg_pixel >= bounds[DAY]):
        day_label = 'Day_Time'        
        ratio = NORMAL_BG_RATIO
        threshold = NORMAL_THRESHOLD
    else: # transition moment --> sunset/sunrise
        day_label = 'Sunset / Sunrise'        
        ratio = RAPID_BG_RATIO
        threshold = NORMAL_THRESHOLD
        
    print(day_label)
    print("Updating ratio to {}".format(ratio))
    
    return ratio, threshold

#==============================================================================
# ----------------------COMPUTE PIXEL INTENSITY AVERAGE------------------------
#
#   It takes 100 random points from each square placed in the frame: there
#   are five squares placed respectively in the center and in the four corners
#   of the frame. Dimension of each square: 80x80
#
#   PARAMETERS:
#
#   - frame     -->    frame where taking these random points
#
#   RETURN:
#
#   - avg_pixel -->    computed average of the pixel intensity of the frame
#
#==============================================================================
#def computePixelIntensityAverage(frame):
#    points_value = []
#    points_coord = []
#    
#    for i in range(1,100):
#        
#        row_left_up = int(np.random.uniform(30, 110))
#        column_left_up= int(np.random.uniform(30, 110))
#        points_coord.append([row_left_up, column_left_up])
#        
#        row_left_down = int(np.random.uniform(250, 330))
#        column_left_down = int(np.random.uniform(30, 110))
#        points_coord.append([row_left_down, column_left_down])        
#        
#        row_center = int(np.random.uniform(180-40, 180+40))
#        column_center = int(np.random.uniform(320-40, 320+40))
#        points_coord.append([row_center, column_center])
#        
#        row_right_up = int(np.random.uniform(30, 110))
#        column_right_up= int(np.random.uniform(530, 610))
#        points_coord.append([row_right_up, column_right_up])        
#        
#        row_right_down = int(np.random.uniform(250, 330))
#        column_right_down= int(np.random.uniform(530, 610))
#        points_coord.append([row_right_down, column_right_down])                       
#        
#        points_value.append(frame[row_center][column_center])
#        points_value.append(frame[row_left_down][column_left_down])
#        points_value.append(frame[row_left_up][column_left_up])
#        points_value.append(frame[row_right_up][column_right_up])
#        points_value.append(frame[row_right_down][column_right_down])
#    
#    
#    drawPoints(frame, points_coord) 
#    avg_pixel = int(np.mean(points_value))
#    
#    return avg_pixel
#
##==============================================================================
## ---------------------SQUARES FUNCTIONS--------------------------------------
##==============================================================================
#def drawPoints(frame, points):
#    
#    temp = np.copy(frame)
#    
#    for point in points:
#        x = point[1]
#        y = point[0]
#        
#        temp[y][x] = 255
#        
##    showImage(temp)
#
#def drawAllRectangles(frame):
#    # Upper left
#    temp = drawRectangle(frame, 30, 110, 30, 110)
#    # Lower left 
#    temp = drawRectangle(temp, 30, 110, 250, 330)
#    # Upper right
#    temp = drawRectangle(temp, 530, 610, 30, 110)
#    # Lower right
#    temp = drawRectangle(temp, 530, 610, 250, 330)
#    # Center
#    temp = drawRectangle(temp, 280, 360, 140, 220)
#    
#    return temp
#
#def drawRectangle(frame, xA, xB, yA, yB):
#
#    temp = np.copy(frame)
##    for i in range(yA, yB):   
#    for j in range(xA, xB):
#        temp[yA][j] = 255
#        temp[yB][j] = 255
#        
#    for j in range(yA, yB):
#        temp[j][xA] = 255
#        temp[j][xB] = 255
#        
#    return temp;
##==============================================================================
## 
##==============================================================================
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

#%% WEIGHTED GAUSSIAN UPDATE
#==============================================================================
# Weight factor
# w = 3
# 
# new_means = new_mean * w + np.mean(old_means) * len(old_means)
# 
#==============================================================================
#==============================================================================
#    -Get mean of the frame where foreground is detecting the transition time
#    -Use that mean to evaluate day/night probability
#    -Use this probability to check if the actual mean belongs to this probability range
#    -Update ratio and threshold
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


