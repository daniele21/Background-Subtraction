# -*- coding: utf-8 -*-
"""
Created on Wed May  8 13:29:56 2019

@author: daniele
"""

#%% IMPORTS
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm

from gaussians import generateDayNightGaussians, initGaussian, plotDayNightGaussian

NORMAL_THRESHOLD = 70
NIGHT_THRESHOLD = 140
#%%
all_means = []
all_means.append(means1)
all_means.append(means2)
all_means.append(means3)
all_means.append(means4)
all_means.append(means5)

#%% Compute Gaussians

def gaussianAllDay(means):
    day = []
    night = []    
    
    for mean in means:
        mid_point = int((max(means) - min(means))/2)
        split = mid_point + min(means)
        
        if(mean > split):        
            day.append(mean)
        elif(mean < split):
            night.append(mean)
            
    # Reconstruction of day gaussian and night gaussian
    mu_day = int(np.mean(day))
    sigma_day = np.std(day)
    gauss_day = norm(mu_day, sigma_day)    

    mu_night = int(np.mean(night))
    sigma_night = np.std(night)
    gauss_night = norm(mu_night, sigma_night)
    
    x_axis = np.linspace(0,255,255)     #255 is the max luminosity    
    plt.xlim(10,150)
    
    y_day = gauss_day.pdf(x_axis)
    y_night = gauss_night.pdf(x_axis)              # get the norm.pdf for x interval 

#    plt.plot(x_axis, y_day, color = 'y')
#    plt.plot(x_axis, y_night, color = 'b')        
#    plt.show()
    
    return gauss_day, gauss_night, y_day, y_night
#%% MAIN

x_axis = np.linspace(0,255,255)
y_days = []
y_nights = []
gauss_days = []
gauss_nights = []

for means in all_means:
    gauss_day, gauss_nigth, y_day, y_night = gaussianAllDay(means)
    gauss_days.append(gauss_day)
    gauss_nights.append(gauss_nigth)
    y_days.append(y_day)
    y_nights.append(y_night)

y_overall_day = np.zeros_like(x_axis)
y_overall_night = np.zeros_like(x_axis)

for i in range(0, len(y_days)):    
    y_overall_day = y_overall_day + gauss_days[i].pdf(x_axis)
    y_overall_night = y_overall_night + gauss_nights[i].pdf(x_axis)

plt.xlim(10, 150)
plt.plot(x_axis, y_overall_day, color = 'orange')
plt.plot(x_axis, y_overall_night, color = 'b')
plt.show()


#%%
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
    y_night = gauss_night.pdf(x_axis)              # get the norm.pdf for x interval 

    plt.plot(x_axis, y_day, color = 'orange')
    plt.plot(x_axis, y_night, color = 'b')        
    plt.show()


#%% For single Means

# given intensity value get the probability
pixel_intensity = 96
probability = gauss_days[4].cdf(pixel_intensity)
print("Probability\t--> \t{}\nPixel intensity --> \t{}".format(probability, pixel_intensity))

pixel_intensity = 100
probability = gauss_nights[4].cdf(pixel_intensity)
print("Probability\t--> \t{}\nPixel intensity --> \t{}".format(probability, pixel_intensity))

#%%
def plotGaussian(gauss_distr, x_axis):
    y_axis = gauss_distr.pdf(x_axis)
    
#    plt.xlim(10,150)
    plt.plot(x_axis, y_axis, color = 'r')
#    plt.fill_between(x_axis, 0, y_axis, color = '#b80303')

#%%

#%%

##%% OLD VERSION
#MEAN = 100
#STD = 3
#SHIFT = -3
#x = np.linspace(0,255,255)
#
#gauss_distr = norm(MEAN,STD)
#gauss_distr_shifted = norm(MEAN+SHIFT,STD)
#
#ripartition = gauss_distr.pdf(x)
#density = gauss_distr.cdf(x)
#
#density_shifted = gauss_distr_shifted.cdf(x)
## =============================================================================
##  SETTING 1               SETTING 2
##
##  K = 3,6
##  POWER = 2.61
##  FLEX = 1
## =============================================================================
#K = 5
#POWER = 5.5
#FLEX = 1
#
#get_sigmoid = lambda x: K / (1 + np.exp(-x**FLEX))**POWER
##sigmoid = get_sigmoid(density)
#sigmoid = get_sigmoid(density_shifted)
##OFFSET = max(sigmoid)
## =============================================================================
# #print('large: {}'.format(max(sigmoid)-min(sigmoid)))
# #print('min: {}'.format(min(sigmoid)))
## =============================================================================
##sigmoid = sigmoid - OFFSET
#ratio = 1-sigmoid
##plt.plot(x2,(1-sigmoid )* (max(ripartition)),'b')
#
#BOUND = 100
#
#pixel_intensity = BOUND
#density_value = ripartition[pixel_intensity]
#density_shifted_value = ratio[pixel_intensity]
##density_value = a.cdf(pixel_intensity)
#
#
#plt.xlim(75, 125)
#plt.plot(ripartition, color = 'r')
#plt.scatter(pixel_intensity, density_value, color = 'g')
#plt.show()
#plt.xlim(75, 125)
#plt.plot(x,ratio ,'b')
#plt.scatter(pixel_intensity, density_shifted_value, color = 'g')
#plt.grid()
#print('pixel intensity : {}\nvalue : {}'.format(pixel_intensity, density_value))
#

#%% NEW VERSION
MEAN = 100
STD = 3
SHIFT = -5
MIN_VALUE = 0.1
x = np.linspace(0,255,255)

gauss_distr = norm(MEAN,STD)
gauss_distr_shifted = norm(MEAN+SHIFT,STD)

ripartition = gauss_distr.pdf(x)

density_shifted = gauss_distr_shifted.cdf(x)

ratio1 = 1-density_shifted
ratio2 = density_shifted
#plt.plot(x2,(1-sigmoid )* (max(ripartition)),'b')

BOUND = 95

ratio1 = MIN_VALUE + ratio1*0.85
ratio2 = ratio2*0.85

pixel_intensity = BOUND
ripartition_prob = ripartition[pixel_intensity]
density_shifted_prob1 = ratio1[pixel_intensity]
density_shifted_prob2 = ratio2[pixel_intensity]
#density_value = gauss_distr_shifted.cdf(pixel_intensity)


plt.xlim(75, 125)
plt.plot(ripartition, color = 'r')
plt.scatter(pixel_intensity, ripartition_prob, color = 'g')
plt.show()
plt.xlim(75, 125)
plt.plot(x,ratio1 ,'b')
#print('max : {}\nmin: {}'.format(max(ratio1), min(ratio1)))
plt.scatter(pixel_intensity, density_shifted_prob1, color = 'g')
plt.plot(x,ratio2 ,'g')
#print('max : {}\nmin: {}'.format(max(ratio1), min(ratio1)))
plt.scatter(pixel_intensity, density_shifted_prob2, color = 'g')
plt.grid()
print('pixel intensity : {}\nvalue_density : {}\nratio : {}'.format(
    pixel_intensity, ripartition_prob, density_shifted_prob1))
 
#%%
x_axis = np.linspace(-10,30, 1000)

a = norm(0,1)
a = a.cdf(x_axis)

b = norm(10,1)
b = 1-b.cdf(x_axis)

idx = np.argwhere(np.diff(np.sign(a - b)) != 0)
idx = idx[0][0]
#plt.scatter(x_axis[idx], a[idx], c='g')

plt.plot(x_axis[0:idx], a[0:idx], c='r')
plt.plot(x_axis[idx:1000], b[idx:1000], c='b')

#%%

    mean_day = 110
    mean_night = 65

    threshold = np.zeros(255)
    
    for i in range(0,255):
#      print(i)
      if(i < mean_night):
        threshold[i] = NIGHT_THRESHOLD
      elif(i > mean_day):
        threshold[i] = NORMAL_THRESHOLD
      else:
        x1 = mean_night
        x2 = mean_day
        y1 = NIGHT_THRESHOLD
        y2 = NORMAL_THRESHOLD
        m = (y2-y1)/(x2-x1)
        q = y1 - m * x1 
        
        y = m*i + q
        
        threshold[i]=(y)
        
    
    x = np.linspace(0, 255, 1000)
    
#    plt.plot(threshold, c='black')
        
    K = NIGHT_THRESHOLD - NORMAL_THRESHOLD
    POWER = 1
    FLEX = 1
    
    get_sigmoid = lambda x: K / (1 + np.exp(-x**FLEX))**POWER
    sigmoid = get_sigmoid(x-50)
    plt.plot(x, NORMAL_THRESHOLD + sigmoid)
    
#%%
    mean_day = 110
    mean_night = 65
    
    mean = mean_night + (mean_day - mean_night)
    std = 15
    
    x_axis = np.linspace(0,255,255)
    sigmoid = 1 - norm(mean, std).cdf(x_axis)
    
    plt.plot(x_axis, sigmoid)
  