###############################################################################
# Asset Pricing in Discrete Time
# Description: This file allows us to make a portfolio and make changes to it
# Author: Pranay Gundam
###############################################################################

import Options
import Discrete_Pricing

class Portfolio(object):
    def __init__(self, assets, constants):
        self.port = dict()
        for i in range(len(assets)):
            self.port[assets[i]] = constants[i]
        
    def getAssets(self):
        return self.port.keys()
    
    def getConstants(self):
        return self.port.values()

    def getAssetConstantPair(self):
        return self.port.items()    

    def addAsset(self, asset, n):
        if n <= 0: 
            print("You can't add a non-positive number of assets")
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
    # domain each time.
    def calcPortfolio(self):
        portval = [dict()] * self.get
        for asset in self.getAssetConstantPair():
            pass
        return portval

