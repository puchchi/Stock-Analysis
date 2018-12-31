import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kRSI():

    def __init__(self):
        #do nothing
        print "In kRSI class"

    def CalculateRSI(self, avgGain, avgLoss):
        if avgLoss == 0:
            return 100

        rs = avgGain / abs(avgLoss)
        rsi = 100 - ( 100 / ( 1 + rs))
        return rsi

    def Calculate(self, dataFrame):
        #####  ALGORITHM #####
        #               100
        # RSI = 100 - --------
        #              1 + RS

        # RS = Average Gain / Average Loss

        # The very first calculations for average gain and average loss are simple 14-period averages.
        # First Average Gain = Sum of Gains over the past 14 periods / 14.
        # First Average Loss = Sum of Losses over the past 14 periods / 14

        # The second, and subsequent, calculations are based on the prior averages and the current gain loss:
        # Average Gain = [(previous Average Gain) x 13 + current Gain] / 14.
        # Average Loss = [(previous Average Loss) x 13 + current Loss] / 14.

        close = dataFrame['Close']
        change = close.diff()
        change = change.fillna(0)

        firstAvgGain = 0
        firstAvgLoss = 0
        rsiSeries = pd.Series()

        for i in range(14):
            # Appending first 14 dummy value to RSI series
            rsiSeries = rsiSeries.append(pd.Series({dataFrame.index[i]: 0}))
            if change[i]>0:
                firstAvgGain = firstAvgGain + change[i]
            else:
                firstAvgLoss = firstAvgLoss + change[i]

        firstAvgGain = firstAvgGain/14
        firstAvgLoss = firstAvgLoss/14

        rsiValue = self.CalculateRSI(firstAvgGain, firstAvgLoss)
        rsiSeries[13] = rsiValue

        avgGain = firstAvgGain;
        avgLoss = firstAvgLoss
        for i in range(14, close.count()):
            if change[i]>0:
                avgGain = ((avgGain * 13) + change[i]) / 14
            else:
                avgLoss = ((avgLoss * 13) + change[i]) / 14

            rsiValue = self.CalculateRSI(avgGain, avgLoss)
            rsiSeries = rsiSeries.append(pd.Series({dataFrame.index[i]: rsiValue}))

        #print rsiSeries
        return rsiSeries
