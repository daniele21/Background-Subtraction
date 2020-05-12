# Background-Subtraction

## Description:
Background Subtraction is a Computer Vision problem of understanding and concretely detecting what is background in a scene, clean from any kind of foreground of that scene. It is applied to a video as input and it suggests frame by frame the detected background.
Gaussian Mixture Models (GMM) are able to provide a good solution for the background subtractrion problem: for each frame of a video, the GMM can reproduce the background behind the foreground.

## Goal:
The goal is to improve the GMM, in order to overcome its limits: GMM is not enough adaptive to the change of natural light. This project provides the AGM (Adaptive Gaussian Model), making the GMM adaptive to the change of natural lights.

## Domain:
Highway 24h Video taken by 'Autostrade per l'Italia' from https://www.autostrade.it/.

## GMM Limits:
