# Background-Subtraction
Adaptive Gaussians Model (AGM) applied to the Gaussian Mixture Model (GMM) for the background subtraction

Background Subtraction is a Computer Vision problem
of understanding and concretely detecting what is
background in a scene, clean from any kind of
foreground of that scene. It is applied to a video as input
and it suggests frame by frame the detected background.

We tried to use the one
based on gaussians model, called Gaussian Mixture
Model (GMM), and make it adaptive to a 24h video taken from 
some italian highway.

Results:

Adaptive Gaussian Model has API(Average Pixel Intensity) values very near to the real one(Original frame).
Gaussian Mixture Model has API that updates slower than AGM. These are two examples during SUNSET and SUNRISE

![Comparison of API(Average Pixel Intensity) relatives to AGM - GMM - Original frame](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM%2CAGM_sunrise_trend.png)


![Comparison of API(Average Pixel Intensity) relatives to AGM - GMM - Original frame](https://github.com/daniele21/Background-Subtraction/blob/master/Results/GMM%2CAGM_sunset_trend.png)
