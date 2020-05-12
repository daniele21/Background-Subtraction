#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  1 15:00:34 2019

@author: daniele
"""

#%% IMPORTS
import numpy as np
import cv2 as cv

#%% CONSTANTS

WHITE_PIXEL = 255

# N POINTS FOR EACH SQUARE
N_POINTS = 100

# KEYS
UPPER_LEFT = 'upper-left'
UPPER_RIGHT = 'upper-right'
DOWN_LEFT = 'down-left'
DOWN_RIGHT = 'down-right'
CENTER = 'center'

# SQUARE UPPER_LEFT
ROW_START_UL, COLUMN_START_UL = 30
ROW_END_UL, COLUMN_END_UL = 110

# SQUARE DOWN_LEFT
ROW_START_DL = 250
ROW_END_DL = 330
COLUMN_START_DL = 30
COLUMN_END_DL = 110

# SQUARE CENTER
ROW_START_C = 140
ROW_END_C = 220
COLUMN_START_C = 280
COLUMN_END_C = 360

# SQUARE UPPER_RIGHT
ROW_START_UR = 30
ROW_END_UR = 110
COLUMN_START_UR = 530
COLUMN_END_UR = 610

# SQUARE RIGHT_DOWN
ROW_START_DR = 250
ROW_END_DR = 330
COLUMN_START_DR = 530
COLUMN_END_DR = 610

#%%

def drawPoints(frame, points):
    
    temp = np.copy(frame)
    
    for point in points:
        x = point[1]
        y = point[0]
        
        temp[y][x] = 255
        

class RandomPoints():
    
    def __init__(self, frame):
        
#        DICT: points={KEY : value}
        self.points_coord = dict()
        self.frame = frame
        
    
    def generateRandomPixels(self):
        
        for i in range(1, N_POINTS):
            
            row_left_up = int(np.random.uniform(ROW_START_UL, ROW_END_UL))
            column_left_up= int(np.random.uniform(COLUMN_START_UL, COLUMN_END_UL))
            self.points_coord.update({UPPER_LEFT : [column_left_up, row_left_up]})
            
            row_left_down = int(np.random.uniform(ROW_START_DL, ROW_END_DL))
            column_left_down = int(np.random.uniform(COLUMN_START_DL, COLUMN_END_DL))
            self.points_coord.update({DOWN_LEFT : [column_left_down, row_left_down]})
            
            row_center = int(np.random.uniform(ROW_START_C, ROW_END_C))
            column_center = int(np.random.uniform(COLUMN_START_C, COLUMN_END_C))
            self.points_coord.update({CENTER : [column_center, row_center]})
            
            row_right_up = int(np.random.uniform(ROW_START_UR, ROW_END_UR))
            column_right_up= int(np.random.uniform(COLUMN_START_UR, COLUMN_END_UR))
            self.points_coord.update({UPPER_RIGHT : [column_right_up, row_right_up]})
            
            row_right_down = int(np.random.uniform(ROW_START_DR, ROW_END_DR))
            column_right_down= int(np.random.uniform(COLUMN_START_DR, COLUMN_END_DR))
            self.points_coord.update({DOWN_RIGHT : [column_right_down, row_right_down]})
            
        self.drawPoints(self.drawAllRectangles(self.frame), self.points_coord)
    
    def getAveragePixelIntensity(self):
        point_intensities = []
        
        for point in self.points_coord:
            x = point[0]
            y = point[1]
            point_intensities.append(self.frame[x][y])
            
        return int(np.mean(point_intensities))
    
    #==============================================================================
    # ---------------------SQUARES FUNCTIONS--------------------------------------
    #==============================================================================

    def drawAllRectangles(self):
        # Upper left
#        temp = drawRectangle(frame, 30, 110, 30, 110)
        temp = self.drawRectangle(self.frame, COLUMN_START_UL, COLUMN_END_UL,
                                              ROW_START_UL, ROW_END_UL)
        # Down left 
        temp = self.drawRectangle(temp, COLUMN_START_DL, COLUMN_END_DL,
                                              ROW_START_DL, ROW_END_DL)
        # Upper right
        temp = self.drawRectangle(temp, COLUMN_START_UR, COLUMN_END_UR,
                                              ROW_START_UR, ROW_END_UR)
        # Down right
        temp = self.drawRectangle(temp, COLUMN_START_DR, COLUMN_END_DR,
                                              ROW_START_DR, ROW_END_DR)
        # Center
        temp = self.drawRectangle(temp, COLUMN_START_C, COLUMN_END_C,
                                              ROW_START_C, ROW_END_C)
        
        return temp
    
    def drawRectangle(self, xA, xB, yA, yB):
    
        temp = np.copy(self.frame)
    #    for i in range(yA, yB):   
        for j in range(xA, xB):
            temp[yA][j] = WHITE_PIXEL
            temp[yB][j] = WHITE_PIXEL
            
        for j in range(yA, yB):
            temp[j][xA] = WHITE_PIXEL
            temp[j][xB] = WHITE_PIXEL
            
        return temp;
    
    def showImage(image):
        
        while(True):
            cv.imshow("image", image)
            
            k = cv.waitKey(30)
            if(k ==27):
                break
        
        cv.destroyAllWindows()
    #==============================================================================    