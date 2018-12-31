import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kAccumulationNDistributionLine():

    def __init__(self):
        #do nothing
        print "In kADL class"

    def calculate(self, dataFrame):
        #####  FORMULA #####
        #1. Money Flow Multiplier = [(Close  -  Low) - (High - Close)] /(High - Low) 
        #2. Money Flow Volume = Money Flow Multiplier x Volume for the Period
        #3. ADL = Previous ADL + Current Period's Money Flow Volume

        moneyFlowMul = ((dataFrame['Close'] - dataFrame['Low']) - (dataFrame['High'] - dataFrame['Close'])) / (dataFrame['High'] - dataFrame['Low'])
        moneyFlowVolume = moneyFlowMul * dataFrame['Volume']

        previousADL = pd.Series(moneyFlowVolume[1:], index = moneyFlowVolume.index)
        
        # We need to fill 0th entry with 0
        previousADL = previousADL.fillna(0)

        ADL = previousADL + moneyFlowVolume

        return ADL
