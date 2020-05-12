# Background-Subtraction

## Description:
Background Subtraction is a Computer Vision problem of understanding and concretely detecting what is background in a scene, clean from any kind of foreground of that scene. It is applied to a video as input and it suggests frame by frame the detected background.
Gaussian Mixture Models (GMM) are able to provide a good solution for the background subtractrion problem: for each frame of a video, the GMM can reproduce the background behind the foreground.

## Goal:
The goal is to improve the GMM, in order to overcome its limits: GMM is not enough adaptive to the change of natural light. This project provides the AGM (Adaptive Gaussian Model), making the GMM adaptive to the change of natural lights.

## Domain:
Highway 24h Video taken by 'Autostrade per l'Italia' from https://www.autostrade.it/.

# GMM Limits:
## 06:28: the sun has just arisen
### The background detected by the GMM is late, in terms of natural lights
![GMM demo](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM%20limits.png)

### Lights analysis GMM:
This analysis is based on the Average Pixel Intensity (API) and it shows how the detected background adapts to the changing lights (sunset or sunrise).

#### Analysis: GMM provides background subtraction frames that are behind in terms of natural lights 
![GMM result](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM_results.png)
- The red line represents the API for the original frames of the video
- The greed line represents the API for the background detection frames of GMM



# AGM Solution:
## 06:28: the sun has just arisen
### the background detected by the AGM is very similar to the real one, in terms of natural lights
![AGM demo](https://github.com/daniele21/Background-Subtraction/blob/master/Results/AGM%20solution.png)

### Lights Analysis: AGM provides background subtraction frames very near to the real ones
![AGM result](https://github.com/daniele21/Background-Subtraction/blob/master/Results/AGM_results.png)
- The red line represents the API for the original frames of the video
- The greed line represents the API for the background detection frames of AGM

## Comparing the Analysis
![comparison](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM%2CAGM_sunrise_trend.png)


### Video for the sunrise:
#### GMM: ![video GMM](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM.flv)
#### AGM: ![video AGM](https://github.com/daniele21/Background-Subtraction/blob/master/Results/AGM.flv)
