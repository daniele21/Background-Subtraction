# -*- coding: utf-8 -*-
"""
Created on Thu May  9 23:31:52 2019

@author: daniele
"""
#==============================================================================
#%% IMPORT
#==============================================================================
import numpy as np
import cv2 as cv
from scipy.stats import norm
import gaussians_v2 as gauss
from matplotlib import pyplot as plt

DAY = 'day'
NIGHT = 'night'

#%%

def computePixelIntensityAverage(frame):
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
    
    
    drawPoints(drawAllRectangles(frame), points_coord) 
    avg_pixel = int(np.mean(points_value))
    
    return avg_pixel

#==============================================================================
# ---------------------SQUARES FUNCTIONS--------------------------------------
#==============================================================================
def drawPoints(frame, points):
    
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
#==============================================================================
def showImage(frame):
    
    while(True):
        cv.imshow("image", frame)
        
        k = cv.waitKey(30)
        if(k ==27):
            break
        
    cv.destroyAllWindows()

#==============================================================================
#%%
    
    gauss_distr = {DAY: norm(100,3), NIGHT: norm(60,3)}
    X = np.linspace(0,255,255)
    
    
    MEAN_DAY = gauss_distr[DAY].mean()
    STD_DAY = gauss_distr[DAY].std()
    OFFSET_DAY = -2

    MEAN_NIGHT = gauss_distr[NIGHT].mean()+10
    STD_NIGHT = gauss_distr[NIGHT].std()
    OFFSET_NIGHT = -2
    
    RANGE = 0.05
    MIN_VALUE = 0.01
    
    gauss_distr_shifted = {DAY: norm(MEAN_DAY + OFFSET_DAY, STD_DAY),
                           NIGHT: norm(MEAN_NIGHT + OFFSET_NIGHT, STD_NIGHT)}
    
    density_shifted_DAY = gauss_distr_shifted[DAY].cdf(X)
    density_shifted_NIGHT = gauss_distr_shifted[NIGHT].cdf(X)
    densities_shifted = {DAY: density_shifted_DAY, NIGHT: density_shifted_NIGHT}
  
    learning_rate_DAY = MIN_VALUE + (1 - densities_shifted[DAY]) * (RANGE - MIN_VALUE)
    learning_rate_NIGHT = MIN_VALUE + (densities_shifted[NIGHT]) * (RANGE - MIN_VALUE)
    learning_rate = {DAY: learning_rate_DAY, NIGHT: learning_rate_NIGHT}

    gauss.plotLearningRate(learning_rate)
    
#%%
    x_axis = np.linspace(-20, 20, 1000)
    
    g1 = norm(0, 3.2).pdf(x_axis);
    g2 = norm(5, 3.7).pdf(x_axis);
    g3 = norm(-5, 3.1).pdf(x_axis);
    g4 = norm(8, 3.2).pdf(x_axis);
    g5 = norm(-7, 3.5).pdf(x_axis);
    
    plt.plot(x_axis, g1)
    plt.plot(x_axis, g2)
    plt.plot(x_axis, g3)
    plt.plot(x_axis, g4)
    plt.plot(x_axis, g5)
    
    plt.grid()
    plt.show()