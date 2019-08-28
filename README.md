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

![AGM-GMM update light - comparison](https://github.com/daniele21/Background-Subtraction/blob/master/Results/Screenshot%202019-08-28%2020:15:20.png)

![image2](https://github.com/daniele21/Background-Subtraction/blob/master/Results/Screenshot%202019-08-28%2020:15:55.png)

![image3](https://github.com/daniele21/Background-Subtraction/blob/master/Results/Screenshot%202019-08-28%2020:16:23.png)
