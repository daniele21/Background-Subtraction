    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 10:09:54 2019

@author: daniele
"""

# Window Size --> from 1 on 
# Master --> master frame

#%% IMPORTS

from tkinter import Label, Button, Scale
from tkinter import ttk
import tkinter as tk
from GridStructure import GridStruct
from MyScale import MyScale
from LevelWindow import LevelWindow#, WindowController
from ScrollFrame import ScrollFrame

ACTIVE_BG_SLIDER = 'gray'
BG_SLIDER = '#10ce10'
ROWPAD = 6
COLUMNPAD = 6
BG_COLOR = '#90a0be'
PADY = 20
  
def setWindowSize(window_size, master):
    root = master
    
    height_screen = root.winfo_screenheight()
    weight_screen = root.winfo_screenwidth()

    h = int(height_screen/window_size)
    w = int(weight_screen/window_size)
    root.geometry("{}x{}".format(w, h))
    # Gets the requested values of the height and widht.

    # Gets both half the screen width/height and window width/height
    positionX = int(root.winfo_screenwidth()/2 - w/2)
    positionY = int(root.winfo_screenheight()/2 - h/2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionX, positionY))
    
    return root
       
def level1_window_action():
    
#    WindowController(root).pack()   
    
    lv1_window = tk.Toplevel(root)
    lv1_window = setWindowSize(1, lv1_window)
    lv1_window.title('Level-1 Setup')
    
#    print("info: ", lv1_window)
    level1 = LevelWindow(lv1_window, 1)
    level1.pack()
    
    
def level2_window_action():
    
    lv2_window = tk.Toplevel(root)
    lv2_window = setWindowSize(1, lv2_window)
    lv2_window.title('Level-2 Setup')
    
#    print("info: ", lv2_window)
    level2 = LevelWindow(lv2_window, 2)
    level2.pack()
    
def level3_window_action():
    
    lv3_window = tk.Toplevel(root)
    lv3_window = setWindowSize(1, lv3_window)
    lv3_window.title('Level-3 Setup')
    
#    print("info: ", lv3_window)
    level3 = LevelWindow(lv3_window, 3)
    level3.pack()
    
    
    
class MainWindow(tk.Frame):      
    
    def __init__(self, parent):
        super().__init__(parent) # create a frame (self)

        self.mainFrame = ScrollFrame(self)

        self.mainWidgets()

        self.mainFrame.pack()

#    def adaptWindowSize(self, root):
#        self.mainFrame.canvas.bind("<Configure>", self.on_resize)
#        self.mainFrame.canvas.height = self.mainFrame.canvas.winfo_reqheight()
#        self.mainFrame.canvas.width = self.mainFrame.canvas.winfo_reqwidth()
#
#    def on_resize(self,event):
#        # determine the ratio of old width/height to new width/height
#        wscale = float(event.width)/self.width
#        hscale = float(event.height)/self.height
#        self.width = event.width
#        self.height = event.height
#        # resize the canvas 
#        self.config(width=self.width, height=self.height)
#        # rescale all the objects tagged with the "all" tag
#        self.scale("all",0,0,wscale,hscale)

  
    def mainWidgets(self):
        self.title = Label(self.mainFrame.viewPort, text='Rekeep',
                           font=('Comic Sans MS', 20, 'bold'),
                           bg=BG_COLOR).grid(row=0, column=1, pady=PADY)
        
        self.level1_button = Button(self.mainFrame.viewPort, text='Level 1', command=level1_window_action)
        self.level1_button.grid(row=1,column=0)
        
        self.level2_button = Button(self.mainFrame.viewPort, text='Level 2', command=level2_window_action)
        self.level2_button.grid(row=1,column=1)
        
        self.level3_button = Button(self.mainFrame.viewPort, text='Level 3', command=level3_window_action)
        self.level3_button.grid(row=1,column=2)
        
#        self.level3_button1 = Button(self.mainFrame.viewPort, text='Level 3', command=level3_window_action)
#        self.level3_button1.grid(row=1,column=3, padx = 50)
 

if __name__=="__main__":
    root = tk.Tk()
    
    root.title('Rekeep')
#    setWindowSize(2,root)
    
    main = MainWindow(root)
    main.pack(fill="both", expand=True)
#    main.adaptWindowSize(root)
    
    root.mainloop()
    