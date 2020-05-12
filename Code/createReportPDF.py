# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 21:39:38 2019

@author: andre
"""

#%% --------------------------------- IMPORT ---------------------------------

from fpdf import FPDF
from PIL import Image
import numpy as np
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader
import os

webcamInfo = [];
webcamRow = ['./Webcam/web0', 'A01', 'km. 204,0 - Parcheggio Reno']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web1', 'A01', 'km. 43,6 - Ads Somaglia']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web2', 'A08', 'km. 5,6 - Milano Nord itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web3', 'R14', 'km. 2,0 - BO Casalecchio itinere Ovest']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web4', 'A01', 'km. 220,3 - Diramazione A1/A1 VAR']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web5', 'A14', 'km. 154,9 - Galleria Case Bruciate esterna Sud']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web6', 'A04', 'km. 147,9 Svincolo A4/A58 dir Ovest']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web7', 'A04', 'km. 149,5 A4/A58 dir Ovest']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web8', 'A04', 'km. 172,6 Bergamo itinere Ovest']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web9', 'A04', 'km. 215,3 Brescia Ovest itinere Ovest']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web10', 'A13', 'km. 33,0 Ferrara Sud shelter itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web11', 'A14', 'km. 9,0 Bivio A14-Raccordo Casalecchio itinere Sud']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web12', 'A14', 'km. 16,0 Bologna Fiera itinere Sud']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web13', 'A14', 'km. 95,0 Cesena Nord itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web15', 'A08', 'km. 6,5 Villoresi itinere Sud']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web16', 'A08', 'km. 2,2 Milano Fiera itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web17', 'A09', 'km. 20,1 A9/A36 Itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web18', 'A01', 'km. 54,5 Ponte Po']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web19', 'A01', 'km. 139,0 Reggio Emilia itinere Nord']
webcamInfo.append(webcamRow)
webcamRow = ['./Webcam/web20', 'A01', 'km. 194,0 A1/A14 Casalecchio itinere Sud']
webcamInfo.append(webcamRow)

#%% ----------------------------- INITIALIZATION -----------------------------

index = 0
numBG = len(backgrounds)
outputReport = 'report_web4.pdf'
accuracyThreshold = 10
errorThreshold = 12

print('\n')
print('START ANALYSIS')

initializationPage()
print('initiliazation done')

while(index < numBG):
    
    print('Processing image '+ str(index) + '...')
    resultAnalysis(originals[index], backgrounds[index], index, accuracyThreshold, errorThreshold)
    index += 1
    print('Done')

print('ANALYSIS TERMINATED')

print('\nMerge all reports...')

paths = glob.glob('report_num*.pdf')
paths.sort()
mergeReport(outputReport, paths)

print('Done')

for report in paths:
    os.remove(report)
    
os.remove('bg.jpeg')
os.remove('true.jpeg')
os.remove('error.png')

print('Output report ' + outputReport + ' is ready')

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
    
    if(source == './Webcam/web1'):
        key = 0
    if(source == './Webcam/web2'):
        key = 1
    if(source == './Webcam/web3'):
        key = 2
    if(source == './Webcam/web4'):
        key = 3
    if(source == './Webcam/web5'):
        key = 4
    if(source == './Webcam/web6'):
        key = 5
    if(source == './Webcam/web7'):
        key = 6
    if(source == './Webcam/web8'):
        key = 7
    if(source == './Webcam/web9'):
        key = 8   
        
    
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
    
    image_true.save("true.jpeg")
    image_bg.save("bg.jpeg")
    
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
    
    pdf.image("true.jpeg",40,37,130,72)
    
    text = 'Background detected:'
    pdf.cell(0, 7,  txt="{}".format(text), ln=2, border=0,align="L")    
   
    pdf.cell(0, 74, "", ln=2,border=0)
    
    pdf.image("bg.jpeg",40,118,130,72)
    
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