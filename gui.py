###############################################################################
# Asset Pricing in Discrete Time
# Description: This file contains code that makes the user interface
# Author: Pranay Gundam
###############################################################################
from Options import *
from Portfolio import *
from Discrete_Pricing import *
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

        startxlower = mode.width/4
        startxupper = mode.width/2+mode.width/4
        startylower = mode.height/4 + 100
        startyupper = mode.height/4+mode.buttonHeight + 100
        if (event.x >= startxlower and event.x <= startxupper and event.y >= startylower 
            and event.y <= startyupper):
            mode.app.setActiveMode(mode.app.mainApp1)
 

    
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
        font1 = 'ComicSansMS 10 bold'
        text1 = ("This project currently prices options in discrete time. " + 
        "It uses a N-period binomial model with a market \nthat has a bank with interest rate r and a stock" +
        " with initial stock price S_0. Included is code\n to calculate the number of stocks"+
        " held in the replicating portfolio at any given time and also the value of a "+
        "portfolio holding securities (S^0, S^1, ..., S^n)\n with quanities"+
        " (c^1, c^2, ..., c^n). Types of securities supported: " + 
        "Bank, Stock, European Call, European Put, European \nStraddle, American Call"+
        ", American Put, American Straddle, Down and In Barrier, Up and In Barrier, "+
        "Down and Out Barrier, Up and Out Barrier.")

        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill=mode.LightSteelBlue)
        canvas.create_rectangle(20,20, mode.width/12, mode.height/10, 
                                fill = mode.SlateGrey)
        canvas.create_text((mode.width/12 + 20)/2, (mode.height/10 + 20)/2, 
                           text = "Back", fill = 'black', font = font)
        canvas.create_text(mode.width/2, mode.height/2, text = text1, 
                           fill = 'black', font = font1)

class MainApp1(Mode):
    def appStarted(mode):
        mode.portfolio = Portfolio([],[])


        mode.LightSteelBlue = rgbString(176,196,222)
        mode.TextColor = rgbString(0,0,0)
        mode.SlateGrey = rgbString(112,128,144)
        
        mode.isBaseView = True
        mode.isPortView = False
        mode.isEvalView = False

    def mousePressed(mode, event):
        backxlower = 20
        backxupper = mode.width/12
        backylower = 20
        backyupper = mode.height/10
        if (event.x >= backxlower and event.x <= backxupper and event.y >= backylower 
            and event.y <= backyupper):
            mode.isBaseView = True
            mode.isPortView = False
            mode.isEvalView = False
            mode.app.setActiveMode(mode.app.homeMode)

        b1xlower = mode.width- 20 - mode.width/12
        b1xupper = mode.width-20
        b1ylower = 20
        b1yupper = mode.height/10

        b2xlower = mode.width - 40 - mode.width/6
        b2xupper = mode.width - 40 - mode.width/12
        b2ylower = 20
        b2yupper = mode.height/10

        inb1 = (event.x >= b1xlower and event.x <= b1xupper and event.y >= b1ylower 
            and event.y <= b1yupper)

        inb2 = (event.x >= b2xlower and event.x <= b2xupper and event.y >= b2ylower 
            and event.y <= b2yupper)

        if mode.isBaseView:
            if inb1:
                mode.isBaseView = False
                mode.isPortView = True
            elif inb2:
                mode.isBaseView = False
                mode.isEvalView = True
        elif mode.isEvalView:
            if inb1:
                mode.isEvalView = False
                mode.isPortView = True
            elif inb2:
                mode.isEvalView = False
                mode.isBaseView = True
        elif mode.isPortView:
            if inb1:
                mode.isBaseView = True
                mode.isPortView = False
            elif inb2:
                mode.isPortView = False
                mode.isEvalView = True

    def redrawAll(mode, canvas):
        font1 = 'ComicSansMS 15 bold'
        font2 = 'ComicSansMS 7 bold'
        
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill=mode.LightSteelBlue)
        canvas.create_rectangle(20,20, mode.width/12+20, mode.height/10, 
                                fill = mode.SlateGrey)
        canvas.create_text((mode.width/12 + 40)/2, (mode.height/10 + 20)/2, 
                           text = "Back", fill = 'black', font = font1)
        canvas.create_rectangle(mode.width- 20 - mode.width/12, 20, 
                                    mode.width-20, mode.height/10, 
                                    fill = mode.SlateGrey)
        canvas.create_rectangle(mode.width - 40 - mode.width/6, 20, 
                                    mode.width - 40 - mode.width/12, mode.height/10, 
                                    fill = mode.SlateGrey)
        
        if mode.isBaseView:
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "View Portfolio", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Evaluate Portfolio", fill = 'black', font = font2)
        elif mode.isPortView:
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "Main View", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Evaluate Portfolio", fill = 'black', font = font2)        
        elif mode.isEvalView:
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "View Portfolio", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Main View", fill = 'black', font = font2)
        

class PortfolioMaker(ModalApp):
    def appStarted(app):
        app.homeMode = HomeMode()
        app.readMeMode = ReadMeMode()
        app.mainApp1 = MainApp1()
        app.setActiveMode(app.homeMode)


app = PortfolioMaker(width=1200, height=600)
