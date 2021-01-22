###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code that makes the user interface
# Author: Pranay Gundam
###############################################################################

from tkinter import *
from cmu_112_graphics import *
 
#from https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)



class HomeMode(Mode):
    def appStarted(mode):
        mode.buttonHeight = mode.height/6
        mode.LightSteelBlue = rgbString(176,196,222)
        mode.SlateGrey = rgbString(112,128,144)
        
    def mousePressed(mode, event):
        rmxlower = mode.width/4
        rmxupper = mode.width/2+mode.width/4
        rmylower = mode.height/2 + 100
        rmyupper = mode.height/2+mode.buttonHeight + 100
        if (event.x >= rmxlower and event.x <= rmxupper and event.y >= rmylower 
            and event.y <= rmyupper):
            mode.app.setActiveMode(mode.app.readMeMode)

    
    def redrawAll(mode, canvas):
        font = 'ComicSansMS 30 bold'
        font2 = 'ComicSansMS 60 bold'
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill=mode.LightSteelBlue)
        canvas.create_rectangle(mode.width/4, mode.height/4 + 100, 
                                mode.width/2+mode.width/4, mode.height/4+mode.buttonHeight + 100,
                                fill = mode.SlateGrey)
        canvas.create_rectangle(mode.width/4, mode.height/2 + 100, 
                                mode.width/2+mode.width/4, mode.height/2+mode.buttonHeight + 100,
                                fill = mode.SlateGrey)
        canvas.create_text(mode.width//2, mode.height//2 - mode.height/6 + 100, text=f'Start',
                        fill='black', font=font)
        canvas.create_text(mode.width//2, mode.height//2 + mode.height/11 + 100, text=f'Read Me',
                        fill='black', font=font)
        canvas.create_text(mode.width//2,  mode.height/5, text='Portfolio Maker',
                        fill='black', font=font2)
        #canvas.create_text(mode.width//2, mode.height//2, text='See your journal', font=font, fill=mode.manila)

class ReadMeMode(Mode):
    def appStarted(mode):
        mode.LightSteelBlue = rgbString(176,196,222)
        mode.TextColor = rgbString(0,0,0)
        mode.SlateGrey = rgbString(112,128,144)
        
    def mousePressed(mode, event):
        backxlower = 20
        backxupper = mode.width/12
        backylower = 20
        backyupper = mode.height/10
        if (event.x >= backxlower and event.x <= backxupper and event.y >= backylower 
            and event.y <= backyupper):
            mode.app.setActiveMode(mode.app.homeMode)


    def redrawAll(mode, canvas):
        font = 'ComicSansMS 15 bold'
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill=mode.LightSteelBlue)
        canvas.create_rectangle(20,20, mode.width/12, mode.height/10, 
                                fill = mode.SlateGrey)
        canvas.create_text((mode.width/12 + 20)/2, (mode.height/10 + 20)/2, 
                           text = "Back", fill = 'black', font = font)
        

class PortfolioMaker(ModalApp):
    def appStarted(app):
        app.homeMode = HomeMode()
        app.readMeMode = ReadMeMode()
        app.setActiveMode(app.homeMode)


app = PortfolioMaker(width=1200, height=600)
