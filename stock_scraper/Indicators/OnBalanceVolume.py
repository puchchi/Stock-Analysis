import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kOnBalanceVolume():

    def __init__(self):
        #do nothing
        print "In kOBV class"

    def calculate(self, dataFrame):
        #####  FORMULA #####
        # If the closing price is above the prior close price then: 
        # Current OBV = Previous OBV + Current Volume

        # If the closing price is below the prior close price then: 
        # Current OBV = Previous OBV  -  Current Volume

        # If the closing prices equals the prior close price then:
        # Current OBV = Previous OBV (no change)

        # First first obv entry will be 0.
        OBV = pd.Series({dataFrame.index[0] : 0})
        
        for i in range(1, dataFrame["Close"].count()):
            if dataFrame["Close"][i] > dataFrame["Close"][i-1]:
                OBV = OBV.append(pd.Series({dataFrame.index[i] : OBV[i-1] + dataFrame["Volume"][i]}))

            elif dataFrame["Close"][i] < dataFrame["Close"][i-1]:
                OBV = OBV.append(pd.Series({dataFrame.index[i] : OBV[i-1] - dataFrame["Volume"][i]}))

            else:
                OBV = OBV.append(pd.Series({dataFrame.index[i] : OBV[i-1]}))

        return OBV