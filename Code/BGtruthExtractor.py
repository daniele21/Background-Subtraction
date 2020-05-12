# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:32:58 2019

@author: andre
"""
#%%

import numpy as np
import glob
import os
import cv2 as cv
from PIL import Image

# Background subtraction
frame_rate = 5
take_freq = 11
threshold = 40
backgroundRatio = 0.9

# Results Analysis
accuracyThreshold = 10
errorThreshold = 10

source = './Webcam/web12'

videoList = os.listdir(source)

mog = cv.createBackgroundSubtractorMOG2()    
mog.setVarThreshold(threshold)
#mog.setHistory(5)
mog.setBackgroundRatio(backgroundRatio)

videoPaths = []

original_frames = []
bg_frames = []

for video in videoList:
    pathVideo = '{}/{}'.format(source, video)
    videoPaths.append(pathVideo)
    
index = 0
videoPaths.sort
num_video = len(videoPaths)

takeFlag = False;

print('\n')
print('-------------------------------------------------')
print('|\t\t\t\t\t\t|')
print('|\t  START BACKGROUND SUBTRACTION\t\t|')
print('|\t\t\t\t\t\t|')
print('-------------------------------------------------')
print('|\t\t\t\t\t\t|')

index_fg = 0

#for all video
while (index < num_video):
    
    cap = cv.VideoCapture(videoPaths[index])
    
    print('|  '+str(index+1)+'-  load video:   '+videoPaths[index]+'\t|')
    
    index += 1
    
    end = False
    frameCount = 0;
    
    frames = []
        
    while(end == False):
        ret, frame = cap.read()
        if(ret == False):
            end = True
        else:
            if(frameCount%frame_rate==0):
                gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
                frames.append(gray)
        frameCount += 1
        
    cap.release()
    
    for frame in frames:
        
        fg = mog.apply(frame)
        bg = mog.getBackgroundImage()
        
        cv.imshow('Original video', frame) 
        cv.imshow('Background detected', bg)
        cv.imshow('Foreground detected', fg)
    
        # background truth extraction
        
#        count_fg = 0
#        total_pixel = 0
#        threshold_fg = 0.005
#    
#        for row in fg:
#            for el in row:
#                if(el > 0):
#                    count_fg += 1
#                total_pixel +=1
#        
#        ratio_fg = count_fg/total_pixel
#        print("ratio:"+str(ratio_fg))
#        
#        if(ratio_fg < threshold_fg):
#            print("background truth detected")
#           
#            image_fg = Image.fromarray(frame)
#            image_fg.save("image_fg_"+str(index_fg)+".png")
#            index_fg += 1
                    
    
        k = cv.waitKey(30)
        
        # Press ESC to terminate
        # Press S to save background (useless, is done in automatic way)
        
        if(k == 115):
            print("---------------------- SAVE BG ----------------------")
            original_frames.append(frame)
            bg_frames.append(bg)
        
        if(k == 27):
            break
        
        if(k == 115):
            bg_frames.append(bg)
            original_frames.append(frame)
        
    if(k == 27):
        break
        
cv.destroyAllWindows()

print('|\t\t\t\t\t\t|')
print('-------------------------------------------------')
print('|\t\t\t\t\t\t|')
print('|\t  END BACKGROUND SUBTRACTION\t\t|')
print('|\t\t\t\t\t\t|')
print('-------------------------------------------------')

#%%
index = 0
for el in bg_frames:
    image = Image.fromarray(el)
    image.save("bg_"+str(index)+".png")
    index += 1
#%%
index = 0
for el in original_frames:
    image = Image.fromarray(el)
    image.save("original_"+str(index)+".png")
    index += 1

#%%    
    import numpy as np
    import glob
    import os
    import cv2 as cv
    
    from PyPDF2 import PdfFileWriter, PdfFileReader
    from matplotlib import pyplot as plt
    from fpdf import FPDF
    from PIL import Image
    
    webcamInfo = [];
    webcamRow = ['./Webcam/web0', 'A01', 'km. 204,0 - Parcheggio Reno']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web1', 'A01', 'km. 43,6 - Ads Somaglia']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web2', 'A08', 'km. 5,6 - Milano Nord itinere Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web3', 'R14', 'km. 2,0 - BO Casalecchio itinere Ovest']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web5', 'A14', 'km. 154,9 - Galleria Case Bruciate esterna Sud']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web6', 'A04', 'km. 147,9 Svincolo A4/A58 dir Ovest']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web7', 'A04', 'km. 149,5 A4/A58 dir Ovest']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web9', 'A04', 'km. 215,3 Brescia Ovest itinere Ovest']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web10', 'A13', 'km. 33,0 Ferrara Sud shelter itinere Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web11', 'A14', 'km. 9,0 Bivio A14-Raccordo Casalecchio itinere Sud']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web12', 'A14', 'km. 16,0 Bologna Fiera itinere Sud']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web14', 'A14', 'km. 152,1 Galleria Boncio esterna Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web15', 'A08', 'km. 6,5 Villoresi itinere Sud']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web16', 'A08', 'km. 2,2 Milano Fiera itinere Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web17', 'A09', 'km. 20,1 A9/A36 Itinere Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web19', 'A01', 'km. 139,0 Reggio Emilia itinere Nord']
    webcamInfo.append(webcamRow)
    webcamRow = ['./Webcam/web20', 'A01', 'km. 194,0 A1/A14 Casalecchio itinere Sud']
    webcamInfo.append(webcamRow)
    
    initializationPage()
    
    index = 0
    while (index < 4):
        print("analize image"+str(index))
        name = "./bg_truth/bg_"+str(index)+".png"
        image_bg = Image.open(name)
        name = "./bg_truth/bgt_"+str(index)+".png"
        image_truth = Image.open(name)
        image_bg.load()
        image_truth.load()
        data_bg = np.asarray( image_bg, dtype="uint8" )
        data_truth = np.asarray( image_truth, dtype="uint8" )
        resultAnalysis(data_truth,data_bg,index,accuracyThreshold,errorThreshold)
        index+=1
        
    paths = glob.glob('report_num*.pdf')
    paths.sort()
    outputReport = "reportone.pdf"
    mergeReport(outputReport, paths)
        
        
    #%% --------------------------- INITIALIZATION PAGE ---------------------------

####################################################################################
#
# initializationPage()
#
# params: void
#
# return: void
#
####################################################################################

def initializationPage():
    
    pdf = FPDF()
    pdf.set_font("Arial", size=10)
    pdf.add_page()
    
    pdf.set_draw_color(0, 0, 0)
    
    pdf.line(10, 10, 200, 10)
    pdf.line(10, 287, 200, 287)
    pdf.line(10, 10, 10, 287)
    pdf.line(200, 10, 200, 287)
    
    pdf.image("logo.png",79,33,55,55)
    pdf.cell(0,80,"",border=0,ln=2)
    
    text = 'Politecnico di Milano'
    pdf.cell(0, 5, txt="{}".format(text), ln=2, border = 0, align="C")
    text = 'AA 2018 - 2019'
    pdf.cell(0, 5, txt="{}".format(text), ln=2, border = 0, align="C")
    
    pdf.cell(0,8,"",border=0,ln=2)
    text = 'Computer Science and Engineering'
    pdf.cell(0, 5, txt="{}".format(text), ln=2, border = 0, align="C")
    
    pdf.set_font("Arial", size=14)
    text = 'IMAGE ANALYSIS AND COMPUTER VISION PROJECT'
    pdf.cell(0, 15, txt="{}".format(text), ln=2, border = 0, align="C")
    
    pdf.set_font("Arial", "B", size=25)
    text = 'BACKGROUND SUBTRACTION'
    pdf.cell(0, 50, txt="{}".format(text), ln=2, border = 0, align="C")
    
    pdf.set_font("Arial", size=18)
    text = 'Results report:'
    pdf.cell(0, 20, txt="{}".format(text), ln=2, border = 0, align="C")
    
    if(source == './Webcam/web0'):
        key = 0
    if(source == './Webcam/web1'):
        key = 1
    if(source == './Webcam/web2'):
        key = 2
    if(source == './Webcam/web3'):
        key = 3
    if(source == './Webcam/web5'):
        key = 4
    if(source == './Webcam/web6'):
        key = 5
    if(source == './Webcam/web7'):
        key = 6
    if(source == './Webcam/web9'):
        key = 7
    if(source == './Webcam/web10'):
        key = 8 
    if(source == './Webcam/web11'):
        key = 9 
    if(source == './Webcam/web12'):
        key = 10 
    if(source == './Webcam/web14'):
        key = 11
    if(source == './Webcam/web15'):
        key = 12 
    if(source == './Webcam/web16'):
        key = 13 
    if(source == './Webcam/web17'):
        key = 14
    if(source == './Webcam/web19'):
        key = 15
    if(source == './Webcam/web20'):
        key = 16 
        
    
    pdf.set_font("Arial", size=11)
    text = 'Webcam: ' + webcamInfo[key][1] + ' - ' + webcamInfo[key][2]
    pdf.cell(0, 7, txt="{}".format(text), ln=2, border = 0, align="C")
    
    text = 'Threshold = ' + str(threshold)
    pdf.cell(0, 7, txt="{}".format(text), ln=2, border = 0, align="C")
    text = 'Ratio = ' + str(backgroundRatio)
    pdf.cell(0, 7, txt="{}".format(text), ln=2, border = 0, align="C")
    
    pdf.cell(0,15,"",border=0,ln=2)
    
    pdf.set_font("Arial", size=10)
    text = 'Andrea Mazzeo - 895579'
    pdf.cell(0, 5, txt="{}".format(text), ln=2, border = 0, align="C")
    text = 'Daniele Moltisanti - 898977'
    pdf.cell(0, 5, txt="{}".format(text), ln=2, border = 0, align="C")
    
    name = 'report_num00.pdf'
    pdf.output(name)    

#%% ----------------------------- RESULT ANALYSIS -----------------------------

####################################################################################
#
# resultAnalysis (true, bg, index, accuracyThreshold, errorThreshold)
#
# params: true              ->  frame of original video
# params: bg                ->  frame of background detected
# params: index             ->  index of analyzed frame
# params: accuracyThreshold ->  threshold used to compute accuracy
# params: errorThreshold    ->  threshold used to compute error between two frames
#
# return: void
#
####################################################################################

def resultAnalysis(true, bg, index, accuracyThreshold, errorThreshold):
     
    pdf = FPDF()
    
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    
    endRow = len(true)
    endCol = len(true[0])
   
    equal=0
    total=0
    
    pdf.set_font("Arial", "B", size=14)
    text = 'BACKGROUND DETECTION NUMBER ' + str(index) + ' WITH THRESHOLD OF ' + str(accuracyThreshold)
    pdf.cell(0, 12, txt="{}".format(text), ln=2, border=0, align="C")

    image_true = Image.fromarray(true)
    image_bg = Image.fromarray(bg)
    
    image_true.save("true.png")
    image_bg.save("bg.png")
    
    for i in range(1,endRow):
        for j in range(1,endCol):
            if(bg[i][j] in range(true[i][j]-accuracyThreshold,true[i][j]+accuracyThreshold)):
                equal += 1
            total += 1
    
    bg = bg.astype(np.int8)
    true = true.astype(np.int8)
    
    error = np.abs(true-bg)
    
    for i in range(0,endRow):
        for j in range(0,endCol):
            if(error[i][j] < errorThreshold):
                error[i][j] = 0
            else:
                error[i][j] = 255
                
    error = error.astype(np.uint8)
    
    image_error = Image.fromarray(error)
    image_error.save("error.png")
            
    accuracy = equal/total;
    accuracy = round(accuracy*100,2)
    
    pdf.set_font("Arial", size=12)
    text = 'Background detected with accuracy of '+ str(accuracy) + '%'
    pdf.cell(0, 7, txt="{}".format(text), ln=2, border=0,align="L")
    
    text = 'Original frame:'
    pdf.cell(0, 7, txt="{}".format(text), ln=2,border=0, align="L")
    
    pdf.cell(0, 74, "", ln=2,border=0)
    
    pdf.image("true.png",40,37,130,72)
    
    text = 'Background detected:'
    pdf.cell(0, 7,  txt="{}".format(text), ln=2, border=0,align="L")    
   
    pdf.cell(0, 74, "", ln=2,border=0)
    
    pdf.image("bg.png",40,118,130,72)
    
    text = 'Error plotted with threshold of ' + str(errorThreshold) +':'
    pdf.cell(0, 7, txt="{}".format(text), ln=2,border=0, align="L")
    
    pdf.cell(0, 74, "", ln=2,border=0)
    
    pdf.image("error.png",40,199,130,72)
    
    
    indexString = '{0:02}'.format(index+1)
    name = 'report_num'+str(indexString)+'.pdf'
    pdf.output(name)
    
#%% ------------------------------ REPORT MERGER ------------------------------

####################################################################################
#
# mergeReport(output_path, input_paths):
#
# params: output_path  ->  path where store output pdf
# params: input_paths  ->  paths of input reports
#
# return: void
#
####################################################################################
 
def mergeReport(output_path, input_paths):
    pdf_writer = PdfFileWriter()
 
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
 
    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)    
    