###############################################################################
# Asset Pricing in Discrete Time
# Description: This file allows us to make a portfolio and make changes to it
# Author: Pranay Gundam
###############################################################################

import Options
from Discrete_Pricing import *

class Portfolio(object):
    def __init__(self, assets, constants):
        self.port = dict()
        for i in range(len(assets)):
            self.port[assets[i]] = constants[i]
        
    def getAssets(self):
        return list(self.port.keys())
    
    def getConstants(self):
        return list(self.port.values())

    def getAssetConstantPair(self):
        return list(self.port.items())    

    def addAsset(self, asset, n):
        if n <= 0: 
            print("You can't add a non-positive number of assets")
        elif False:
            pass # remember to do safety checking here that the asset added has
                 # the same maturity as all the other assets in the portfolio
        else:
            val = self.port.setdefault(asset, 0)
            self.port[asset] = val+n
        
    def removeAsset(self, asset, n):
        if n <= 0:
            print ("You can't remove a non-positive number of assets")
        elif self.port.get(asset, -1) == -1:
            print("Asset is not included in this portfolio")
        else:
            val = self.port.setdefault(asset)
            self.port[asset] = val-n
        
        if self.port[asset] <= 0: self.port.pop(asset)

    # Can make this a bit more efficient by making sure we don't calculate the
    # domain each time (now that I think about it this doesn't make sense 
    # because each asset has a different underlying). Note we require that
    # each asset in the portfolio has the same "maturity time".
    def calcPortfolio(self):
        # I will do this in a unrefined way for now and modify for later

        assets = self.getAssets()
        constants = self.getConstants()

        if assets == []:
            return []

        placer1 = pricingCalc(assets[0])
        portval = [0] * (assets[0].getMaturity()+1)

        for n in range(len(portval)):
            portval[n] = dict()
            for state in placer1[n]:    
                portval[n][state[0]] = placer1[n][state] * constants[0]
            

        for num in range(1,len(assets)):
            placer2 = pricingCalc(assets[num])
            for n in range(len(portval)):
                for state in placer2[n]:
                    portval[n][state[0]] += placer2[n][state] * constants[num]

        return portval

