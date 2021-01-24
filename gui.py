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
#from Testing import *

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
        #mode.portfolio = testPort()
        mode.porteval = []
        mode.banks = []
        mode.stocks = []
        mode.eurocall = []
        mode.europut = []
        mode.eurostraddle = []
        mode.amercall = []
        mode.amerput = []
        mode.amerstraddle = []
        mode.downandin = []
        mode.downandout = []
        mode.upandin = []
        mode.upandout = []
        
        mode.currAsset = 0


        mode.LightSteelBlue = rgbString(176,196,222)
        mode.TextColor = rgbString(0,0,0)
        mode.SlateGrey = rgbString(112,128,144)
        mode.manila = rgbString(250, 240, 190)
        mode.assetColor = mode.manila

        mode.isBaseView = True
        mode.isPortView = False
        mode.isEvalView = False
        mode.isRemoveMode = False
        mode.isSelectMode = False
        mode.isDisplayMode = False

    def mousePressed(mode, event):
        x = event.x
        y = event.y

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
                mode.porteval = mode.portfolio.calcPortfolio()

            stockxlower = mode.width/2 - 150
            stockxupper = mode.width/2 - 50
            stockylower = mode.height/5
            stockyupper = mode.height/5 + 30
            instock = (x >= stockxlower and x <= stockxupper and 
                       y >= stockylower and y <= stockyupper)

            if instock:
                initPrice = mode.getUserInput("What is the stock's initial price?")
                upFactors = mode.getUserInput("What are the stock's up factors? (enter them comma separated)")
                downFactors = mode.getUserInput("What are the stock's down factors? (enter them comma separated)")
                uplacer = [float(i) for i in upFactors.split(",")]
                dplacer = [float(i) for i in downFactors.split(",")]
                newStock = Stock(uplacer, dplacer, float(initPrice))
                mode.stocks.append(newStock)
                


            bankxlower = mode.width/2 + 50
            bankxupper = mode.width/2 + 150
            bankylower = mode.height/5
            bankyupper = mode.height/5 + 30
            inbank = (x >= bankxlower and x <= bankxupper and 
                       y >= bankylower and y <= bankyupper)

            if inbank:
                interestRates = mode.getUserInput("What are the interest rates over time? (enter them comma separated)")
                placer = [float(i) for i in interestRates.split(",")]
                newBank = Bank(placer)

                mode.banks.append(newBank)

            eurcallxlower = mode.width/2 - 50
            eurcallxupper = mode.width/2 + 50
            eurcallylower = mode.height/5 + 100
            eurcallyupper = mode.height/5 + 130
            ineurcall = (x >= eurcallxlower and x <= eurcallxupper and 
                       y >= eurcallylower and y <= eurcallyupper)

            if ineurcall:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the European Call's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newEuroCall = EuroCall(strike, maturity, underlying, bank)
                mode.eurocall.append(newEuroCall)
                mode.portfolio.addAsset(newEuroCall, 1)

            eurputxlower = mode.width/2 - 200
            eurputxupper = mode.width/2 - 100
            eurputylower = mode.height/5 + 100
            eurputyupper = mode.height/5 + 130
            ineurput = (x >= eurputxlower and x <= eurputxupper and 
                       y >= eurputylower and y <= eurputyupper)
            if ineurput:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the European Put's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newEuroPut = EuroPut(strike, maturity, underlying, bank)
                mode.europut.append(newEuroPut)
                mode.portfolio.addAsset(newEuroPut, 1)

            eurstraxlower = mode.width/2 + 100
            eurstraxupper = mode.width/2 + 200
            eurstraylower = mode.height/5 + 100
            eurstrayupper = mode.height/5 + 130
            ineurstra = (x >= eurstraxlower and x <= eurstraxupper and 
                       y >= eurstraylower and y <= eurstrayupper)
            if ineurstra:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the European Straddle's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newEuroStraddle = EuroStraddle(strike, maturity, underlying, bank)
                mode.eurostraddle.append(newEuroStraddle)
                mode.portfolio.addAsset(newEuroStraddle, 1)

            amercallxlower = mode.width/2 - 50
            amercallxupper = mode.width/2 + 50
            amercallylower = mode.height/5 + 200
            amercallyupper = mode.height/5 + 230
            inamercall = (x >= amercallxlower and x <= amercallxupper and 
                       y >= amercallylower and y <= amercallyupper)
            if inamercall:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the American Call's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newAmerCall = AmerCall(strike, maturity, underlying, bank)
                mode.amercall.append(newAmerCall)
                mode.portfolio.addAsset(newAmerCall, 1)


            amerputxlower = mode.width/2 - 200
            amerputxupper = mode.width/2 - 100
            amerputylower = mode.height/5 + 200
            amerputyupper = mode.height/5 + 230
            inamerput = (x >= amerputxlower and x <= amerputxupper and 
                       y >= amerputylower and y <= amerputyupper)
            if inamerput:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the American Put's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newAmerPut = AmerPut(strike, maturity, underlying, bank)
                mode.amerput.append(newAmerPut)
                mode.portfolio.addAsset(newAmerPut, 1)


            amerstraxlower = mode.width/2 + 100
            amerstraxupper = mode.width/2 + 200
            amerstraylower = mode.height/5 + 200
            amerstrayupper = mode.height/5 + 230
            inamerstra = (x >= amerstraxlower and x <= amerstraxupper and 
                       y >= amerstraylower and y <= amerstrayupper)
            if inamerstra:
                strike = float(mode.getUserInput("What is the Strike Price?"))
                maturity = int(mode.getUserInput("What is the American Straddle's maturity time?"))
                bankNum = int(mode.getUserInput("Which bank would you like to use?"))
                while bankNum > len(mode.banks):
                    bankNum = int(mode.getUserInput("You chose an invalid bank before, which bank would you like to use?"))
                bank = mode.banks[bankNum-1]
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newAmerStraddle = AmerStraddle(strike, maturity, underlying, bank)
                mode.amerstraddle.append(newAmerStraddle)
                mode.portfolio.addAsset(newAmerStraddle, 1)


            daixlower = mode.width/2 - 150
            daixupper = mode.width/2 - 50
            daiylower = mode.height/5 + 300
            daiyupper = mode.height/5 + 330
            indai = (x >= daixlower and x <= daixupper and 
                       y >= daiylower and y <= daiyupper)
            if indai:
                barrier = float(mode.getUserInput("What would you like the barrier to be?"))
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newdib = Down_In_Barrier(underlying, barrier)
                mode.downandin.append(newdib)
                mode.portfolio.addAsset(newdib, 1)


            daoxlower = mode.width/2 - 300
            daoxupper = mode.width/2 - 200
            daoylower = mode.height/5 + 300
            daoyupper = mode.height/5 + 330
            indao = (x >= daoxlower and x <= daoxupper and 
                       y >= daoylower and y <= daoyupper)
            if indao:
                barrier = float(mode.getUserInput("What would you like the barrier to be?"))
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newdob = Down_Out_Barrier(underlying, barrier)
                mode.downandout.append(newdob)
                mode.portfolio.addAsset(newdob, 1)

            uaixlower = mode.width/2 + 50
            uaixupper = mode.width/2 + 150
            uaiylower = mode.height/5 + 300
            uaiyupper = mode.height/5 + 330
            inuai = (x >= uaixlower and x <= uaixupper and 
                       y >= uaiylower and y <= uaiyupper)
            if inuai:
                barrier = float(mode.getUserInput("What would you like the barrier to be?"))
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newuib = Up_In_Barrier(underlying, barrier)
                mode.upandin.append(newuib)
                mode.portfolio.addAsset(newuib, 1)


            uaoxlower = mode.width/2 + 200
            uaoxupper = mode.width/2 + 300
            uaoylower = mode.height/5 + 300
            uaoyupper = mode.height/5 + 330
            inuao = (x >= uaoxlower and x <= uaoxupper and 
                       y >= uaoylower and y <= uaoyupper)
            if inuao:
                barrier = float(mode.getUserInput("What would you like the barrier to be?"))
                assetType = mode.getUserInput("What type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                assetArray = []
                if assetType == "Stock":
                    assetArray = mode.stocks
                elif assetType == "Euro Put":
                    assetArray = mode.europut
                elif assetType == "Euro Call":
                    assetArray = mode.eurocall
                elif assetType == "Euro Straddle":
                    assetArray = mode.eurostraddle
                elif assetType == "American Put":
                    assetArray = mode.amerput
                elif assetType == "American Call":
                    assetArray = mode.amercall
                elif assetType == "American Straddle":
                    assetArray = mode.amerstraddle
                elif assetType == "Down and In Barrier":
                    assetArray == mode.downandin
                elif assetType == "Down and Out Barrier":
                    assetArray == mode.downandout
                elif assetType == "Up and In Barrier":
                    assetArray == mode.upandin
                elif assetType == "Up and Out Barrier":
                    assetArray == mode.upandout

                while assetType == "Bank" or assetNum > len(assetArray):
                    assetType = mode.getUserInput("You made an invalid selection before, what type of asset would you like to be the underlying? (banks cannot be an underlying asset)")
                    assetNum = int(mode.getUserInput(f"Which {assetType} in our portfolio will the underlying be? (exit and view portfolio to see what assets are already in the portfolio)"))
                    assetArray = []
                    if assetType == "Stock":
                        assetArray = mode.stocks
                    elif assetType == "Euro Put":
                        assetArray = mode.europut
                    elif assetType == "Euro Call":
                        assetArray = mode.eurocall
                    elif assetType == "Euro Straddle":
                        assetArray = mode.eurostraddle
                    elif assetType == "American Put":
                        assetArray = mode.amerput
                    elif assetType == "American Call":
                        assetArray = mode.amercall
                    elif assetType == "American Straddle":
                        assetArray = mode.amerstraddle
                    elif assetType == "Down and In Barrier":
                        assetArray == mode.downandin
                    elif assetType == "Down and Out Barrier":
                        assetArray == mode.downandout
                    elif assetType == "Up and In Barrier":
                        assetArray == mode.upandin
                    elif assetType == "Up and Out Barrier":
                        assetArray == mode.upandout
                
                underlying = assetArray[assetNum-1]

                newuob = Up_Out_Barrier(underlying, barrier)
                mode.upandout.append(newuob)
                mode.portfolio.addAsset(newuob, 1)

            removexlower = mode.width/2-100
            removexupper = mode.width/2 + 100
            removeylower = mode.height - 100
            removeyupper = mode.height - 50
            inremove = (x >= removexlower and x <= removexupper and 
                        y >= removeylower and y <= removeyupper)
            if inremove:
                mode.isPortView = True
                mode.isBaseView = False
                mode.isRemoveMode = True

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
                mode.porteval = mode.portfolio.calcPortfolio()
            
            index = -1
            if x >= 10 and x <= 90:
                index = 0
            
            elif x >= 10 + mode.width/8 and x <= mode.width/8 + 90:
                index = 1 

            elif x >= 10 + mode.width/8*2 and x <= mode.width/8*2 + 90:
                index = 2 

            elif x >= 10 + mode.width/8*3 and x <= mode.width/8*3 + 90:
                index = 3 

            elif x >= 10 + mode.width/8*4 and x <= mode.width/8*4 + 90:
                index = 4 

            elif x >= 10 + mode.width/8*5 and x <= mode.width/8*5 + 90:
                index = 5 

            elif x >= 10 + mode.width/8*6 and x <= mode.width/8*6 + 90:
                index = 6 

            elif x >= 10 + mode.width/8*7 and x <= mode.width/8*7 + 90:
                index = 7 


            if y >= 130 and y <= 160 and index >= 0 and index <= len(mode.banks):
                if mode.isRemoveMode:
                    asset2remove = mode.banks.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                else:
                    mode.currAsset = mode.banks[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False
                
            elif y >= 170 and y <= 200 and index >= 0 and index <= len(mode.stocks):
                if mode.isRemoveMode:
                    asset2remove = mode.stocks.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                else:
                    mode.currAsset = mode.stocks[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False
        
            elif y >= 210 and y <= 240 and index >= 0 and index <= len(mode.eurocall):
                if mode.isRemoveMode:
                    asset2remove = mode.eurocall.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                else:
                    mode.currAsset = mode.eurocall[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 250 and y <= 280 and index >= 0 and index <= len(mode.europut):
                if mode.isRemoveMode:
                    asset2remove = mode.europut.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                else:
                    mode.currAsset = mode.europut[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 290 and y <= 320 and index >= 0 and index <= len(mode.eurostraddle):
                if mode.isRemoveMode:
                    asset2remove = mode.eurostraddle.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                else:
                    mode.currAsset = mode.eurostraddle[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 330 and y <= 360 and index >= 0 and index <= len(mode.amerput):
                if mode.isRemoveMode:
                    asset2remove = mode.amerput.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.amerput[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 370 and y <= 400 and index >= 0 and index <= len(mode.amercall):
                if mode.isRemoveMode:
                    asset2remove = mode.amercall.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.amercall[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 410 and y <= 440 and index >= 0 and index <= len(mode.amerstraddle):
                if mode.isRemoveMode:
                    asset2remove = mode.amerstraddle.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.amerstraddle[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 450 and y <= 480 and index >= 0 and index <= len(mode.downandout):
                if mode.isRemoveMode:
                    asset2remove = mode.downandout.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.downandout[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 490 and y <= 520 and index >= 0 and index <= len(mode.downandin):
                if mode.isRemoveMode:
                    asset2remove = mode.downandin.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.downandin[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 530 and y <= 560 and index >= 0 and index <= len(mode.upandin):
                if mode.isRemoveMode:
                    asset2remove = mode.upandin.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.upandin[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False

            elif y >= 570 and y <= 600 and index >= 0 and index <= len(mode.upandout):
                if mode.isRemoveMode:
                    asset2remove = mode.upandout.pop(index)
                    mode.portfolio.removeAsset(asset2remove, 1)
                    
                else:
                    mode.currAsset = mode.upandout[index]
                    mode.isDisplayMode = True
                    mode.isPortView = False


        elif mode.isDisplayMode:
            backxlower = mode.width- 20 - mode.width/12
            backxupper = mode.width- 20
            backylower = 20
            backyupper = mode.height/10
            inback = (x >= backxlower and x <= backxupper and
                      y >= backylower and y <= backyupper)
            if inback:
                mode.isDisplayMode = False
                mode.isPortView = True
            # make shit to identify the asset/bank (the one that we wanna remove
            # and also the one that we wanna select as an underlying)
            


                         
    def mouseMotion(mode, event):
        x = event.x
        y = event.y

        if mode.isPortView:
            pass

        

    def redrawAll(mode, canvas):
        font1 = 'ComicSansMS 15 bold'
        font2 = 'ComicSansMS 7 bold'
        font3 = 'ComicSansMS 25 bold'
        font4 = 'ComicSansMS 18 bold'
        font5 = 'ComicSanseMS 6 bold'
        
        canvas.create_rectangle(0, 0, mode.width, mode.height, 
                                fill=mode.LightSteelBlue)
        canvas.create_rectangle(20,20, mode.width/12+20, mode.height/10, 
                                fill = mode.SlateGrey)
        canvas.create_text((mode.width/12 + 40)/2, (mode.height/10 + 20)/2, 
                           text = "Back", fill = 'black', font = font1)
        
        if mode.isBaseView:
            canvas.create_rectangle(mode.width- 20 - mode.width/12, 20, 
                                    mode.width-20, mode.height/10, 
                                    fill = mode.SlateGrey)
            canvas.create_rectangle(mode.width - 40 - mode.width/6, 20, 
                                    mode.width - 40 - mode.width/12, mode.height/10, 
                                    fill = mode.SlateGrey)
        
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "View Portfolio", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Evaluate Portfolio", fill = 'black', font = font2)
            titletext = "Assets"

            canvas.create_rectangle(mode.width/2 - 150, mode.height/5,
                                mode.width/2 - 50, mode.height/5 + 30, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 - 100, mode.height/5 + 15, 
                               text = "Stock", fill = 'black',
                               font = font2)
            canvas.create_rectangle(mode.width/2 + 50, mode.height/5,
                                mode.width/2 + 150, mode.height/5 + 30, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 + 100, mode.height/5 + 15, 
                               text = "Bank", fill = 'black',
                               font = font2)
            
            canvas.create_rectangle(mode.width/2 - 50, mode.height/5 + 100,
                                mode.width/2 + 50, mode.height/5 + 130, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2, mode.height/5+115,
                               text = "Euro Call", fill = 'black', 
                               font = font2)
            canvas.create_rectangle(mode.width/2 + 100, mode.height/5 + 100,
                                mode.width/2 + 200, mode.height/5 + 130, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 + 150, mode.height/5+115,
                               text = "Euro Straddle", fill = 'black', 
                               font = font2)
            canvas.create_rectangle(mode.width/2 - 200, mode.height/5 + 100,
                                mode.width/2 - 100, mode.height/5 + 130, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 - 150, mode.height/5+115,
                               text = "Euro Put", fill = 'black', 
                               font = font2)

            canvas.create_rectangle(mode.width/2 - 50, mode.height/5 + 200,
                                mode.width/2 + 50, mode.height/5 + 230, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2, mode.height/5+215,
                               text = "American Call", fill = 'black', 
                               font = font2)
            canvas.create_rectangle(mode.width/2 + 100, mode.height/5 + 200,
                                mode.width/2 + 200, mode.height/5 + 230, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 + 150, mode.height/5+215,
                               text = "American Straddle", fill = 'black', 
                               font = font2)
            canvas.create_rectangle(mode.width/2 - 200, mode.height/5 + 200,
                                mode.width/2 - 100, mode.height/5 + 230, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 - 150, mode.height/5+215,
                               text = "American Put", fill = 'black', 
                               font = font2)

            canvas.create_rectangle(mode.width/2 - 150, mode.height/5 + 300,
                                mode.width/2 - 50, mode.height/5 + 330, 
                                fill = 'SpringGreen3')

            canvas.create_text(mode.width/2 - 100, mode.height/5 + 315,
                               text = "Down and In Barrier", fill = "black",
                               font = font2)
            canvas.create_rectangle(mode.width/2 + 50, mode.height/5 + 300,
                                mode.width/2 + 150, mode.height/5 + 330, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 + 100, mode.height/5 + 315,
                               text = "Up and In Barrier", fill = "black",
                               font = font2)
            canvas.create_rectangle(mode.width/2 - 300, mode.height/5 + 300,
                                mode.width/2 - 200, mode.height/5 + 330, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 - 250, mode.height/5 + 315,
                               text = "Down and Out Barrier", fill = "black",
                               font = font2)
            canvas.create_rectangle(mode.width/2 + 200, mode.height/5 + 300,
                                mode.width/2 + 300, mode.height/5 + 330, 
                                fill = 'SpringGreen3')
            canvas.create_text(mode.width/2 + 250, mode.height/5 + 315,
                               text = "Up and Out Barrier", fill = "black",
                               font = font2)

            canvas.create_rectangle(mode.width/2-100, mode.height - 100,
                                    mode.width/2 + 100, mode.height - 50,
                                    fill = 'IndianRed3')
            canvas.create_text(mode.width/2, mode.height- 75,
                               text = "Remove Asset", font = font4, 
                               fill = 'black')

            

        elif mode.isPortView:
            canvas.create_rectangle(mode.width- 20 - mode.width/12, 20, 
                                    mode.width-20, mode.height/10, 
                                    fill = mode.SlateGrey)
            canvas.create_rectangle(mode.width - 40 - mode.width/6, 20, 
                                    mode.width - 40 - mode.width/12, mode.height/10, 
                                    fill = mode.SlateGrey)
        
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "Main View", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Evaluate Portfolio", fill = 'black', font = font2)        
            titletext = "Portfolio View"
            
            if mode.isRemoveMode or mode.isSelectMode:
                titletext = "Select an Asset"


            for banknum in range(len(mode.banks)):
                canvas.create_rectangle(10+mode.width/8*banknum, 130,
                                        mode.width/8*banknum+90, 160,
                                        fill = mode.assetColor)
                newText = f'Bank {banknum+1}'
                canvas.create_text(50 + mode.width/8*banknum, 145, 
                                   text = newText, fill = 'black',
                                   font = font5)
            for stocknum in range(len(mode.stocks)):
                canvas.create_rectangle(10+mode.width/8*stocknum, 170,
                                        mode.width/8*stocknum+90, 200,
                                        fill = mode.assetColor)
                newText = f'Stock {stocknum+1}'
                canvas.create_text(50 + mode.width/8*stocknum, 185, 
                                   text = newText, fill = 'black',
                                   font = font5)
            
            for eurocallnum in range(len(mode.eurocall)):
                canvas.create_rectangle(10+mode.width/8*eurocallnum, 210,
                                        mode.width/8*eurocallnum+90, 240,
                                        fill = mode.assetColor)
                newText = f'Euro Call {eurocallnum+1}'
                canvas.create_text(50 + mode.width/8*eurocallnum, 225, 
                                   text = newText, fill = 'black',
                                   font = font5)
            
            for europutnum in range(len(mode.europut)):
                canvas.create_rectangle(10+mode.width/8*europutnum, 250,
                                        mode.width/8*europutnum+90, 280,
                                        fill = mode.assetColor)
                newText = f'Euro Put {europutnum+1}'
                canvas.create_text(50 + mode.width/8*europutnum, 265, 
                                   text = newText, fill = 'black',
                                   font = font5)
            
            for eurostraddlenum in range(len(mode.eurostraddle)):
                canvas.create_rectangle(10+mode.width/8*eurostraddlenum, 290,
                                        mode.width/8*eurostraddlenum+90, 320,
                                        fill = mode.assetColor)
                newText = f'Euro Straddle {eurostraddlenum+1}'
                canvas.create_text(50 + mode.width/8*eurostraddlenum, 305, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for amerputnum in range(len(mode.amerput)):
                canvas.create_rectangle(10+mode.width/8*amerputnum, 330,
                                        mode.width/8*amerputnum+90, 360,
                                        fill = mode.assetColor)
                newText = f'Amer Put {amerputnum+1}'
                canvas.create_text(50 + mode.width/8*amerputnum, 345, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for amercallnum in range(len(mode.amercall)):
                canvas.create_rectangle(10+mode.width/8*amercallnum, 370,
                                        mode.width/8*amercallnum+90, 400,
                                        fill = mode.assetColor)
                newText = f'Amer Call {amercallnum+1}'
                canvas.create_text(50 + mode.width/8*amercallnum, 385, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for amerstraddlenum in range(len(mode.amerstraddle)):
                canvas.create_rectangle(10+mode.width/8*amerstraddlenum, 410,
                                        mode.width/8*amerstraddlenum+90, 440,
                                        fill = mode.assetColor)
                newText = f'Amer Straddle {amerstraddlenum+1}'
                canvas.create_text(50 + mode.width/8*amerstraddlenum, 425, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for daonum in range(len(mode.downandout)):
                canvas.create_rectangle(10+mode.width/8*daonum, 450,
                                        mode.width/8*daonum+90, 480,
                                        fill = mode.assetColor)
                newText = f'Down and Out {daonum+1}'
                canvas.create_text(50 + mode.width/8*daonum, 465, 
                                   text = newText, fill = 'black',
                                   font = font5)
            
            for dainum in range(len(mode.downandin)):
                canvas.create_rectangle(10+mode.width/8*dainum, 490,
                                        mode.width/8*dainum+90, 520,
                                        fill = mode.assetColor)
                newText = f'Down and In {dainum+1}'
                canvas.create_text(50 + mode.width/8*dainum, 505, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for uainum in range(len(mode.upandin)):
                canvas.create_rectangle(10+mode.width/8*uainum, 530,
                                        mode.width/8*uainum+90, 560,
                                        fill = mode.assetColor)
                newText = f'Up and In {uainum+1}'
                canvas.create_text(50 + mode.width/8*uainum, 545, 
                                   text = newText, fill = 'black',
                                   font = font5)

            for uaonum in range(len(mode.downandin)):
                canvas.create_rectangle(10+mode.width/8*uaonum, 570,
                                        mode.width/8*uaonum+90, 600,
                                        fill = mode.assetColor)
                newText = f'Up and Out {uaonum+1}'
                canvas.create_text(50 + mode.width/8*uaonum, 585, 
                                   text = newText, fill = 'black',
                                   font = font5)
                

        elif mode.isEvalView:
            canvas.create_rectangle(mode.width- 20 - mode.width/12, 20, 
                                    mode.width-20, mode.height/10, 
                                    fill = mode.SlateGrey)
            canvas.create_rectangle(mode.width - 40 - mode.width/6, 20, 
                                    mode.width - 40 - mode.width/12, mode.height/10, 
                                    fill = mode.SlateGrey)
        
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "View Portfolio", fill = 'black', font = font2)
            canvas.create_text((2*mode.width - 80 - mode.width/4)/2, (mode.height/10 + 20)/2, 
                           text = "Main View", fill = 'black', font = font2)
            titletext = "Evaluate Portfolio"

            for i in range(len(mode.porteval)):
                curText = ""
                for state in mode.porteval[i]:
                    curText += f' [({state}): {round(mode.porteval[i][state], 3)}]'
                    
                canvas.create_text(mode.width/2, 100+mode.height/35*i,
                                       text = curText, fill = 'black',
                                       font = font2)

        elif mode.isDisplayMode:
            titletext = "Asset Viewer Mode"
            canvas.create_rectangle(mode.width- 20 - mode.width/12, 20, 
                                    mode.width-20, mode.height/10, 
                                    fill = mode.SlateGrey)
            
            canvas.create_text((2*mode.width - 40 - mode.width/12)/2, (mode.height/10 + 20)/2, 
                           text = "Back To Portfolio", fill = 'black', font = font2)
            
            canvas.create_text(mode.width/2, mode.height/2,
                               text = str(mode.currAsset), fill = 'black',
                               font = font1)


        canvas.create_rectangle(mode.width/2 - mode.width/5, 10, 
                                mode.width/2 + mode.width/5, 90,
                                fill = mode.manila)
        canvas.create_text(mode.width/2, 50, text = titletext, fill = 'black', 
                           font = font3)
        
        

class PortfolioMaker(ModalApp):
    def appStarted(app):
        app.homeMode = HomeMode()
        app.readMeMode = ReadMeMode()
        app.mainApp1 = MainApp1()
        app.setActiveMode(app.homeMode)


app = PortfolioMaker(width=1200, height=610)
