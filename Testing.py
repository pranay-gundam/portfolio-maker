###############################################################################
# Asset Pricing in Discrete Time
# Description: This file is for testing
# Author: Pranay Gundam
###############################################################################

from Discrete_Pricing import *
from Options import *
from Portfolio import *

r1 = [0.1] * 2
u1 = [2] * 2
d1 = [0.5] * 2

bank1 = Bank(r1)
stock1 = Stock(u1, d1, 10)

europut1 = EuroPut(15, 2, stock1, bank1)
europutrng = pricingCalc(europut1)
print("europut1: " + str(europutrng))

eurocall1 = EuroCall(15, 2, stock1, bank1)
eurocallputrng = pricingCalc(eurocall1)
print("eurocall1: " + str(eurocallputrng))

eurostraddle1 = EuroStraddle(15, 2, stock1, bank1)
eurostraddlerng = pricingCalc(eurostraddle1)
print("eurostraddle1: " + str(eurostraddlerng))

amerput1 = AmerPut(15, 2, stock1, bank1)
amerputrng = pricingCalc(amerput1)
print("amerput1: " + str(amerputrng))

amercall1 = AmerCall(15, 2, stock1, bank1)
amercallrng = pricingCalc(amercall1)
print("amercal1: " + str(amercallrng))

amerstraddle1 = AmerStraddle(15, 2, stock1, bank1)
amerstraddlerng = pricingCalc(amerstraddle1)
print("amerstraddle1: " + str(amerstraddlerng))

portfolio1 = Portfolio([europut1, eurocall1, amerput1], [2,1,2])
portvalue1 = portfolio1.calcPortfolio()
print("portvalue1: " + str(portvalue1))