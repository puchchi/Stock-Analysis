import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

import pandas as pd
from scraper.utility import *
from MainDriver.IndicatorTester.IndicatorTesterClass import kIndicatorTesterClass

class kMACDIndicatorTesting(kIndicatorTesterClass):

    def __init__(self, symbol, noOfDays=3):
        self.symbol = symbol
        self.filename = CSV_DATA_DIRECTORY + symbol + CSV_INDICATOR_EXTENSTION
        kIndicatorTesterClass.__init__(self, self.symbol, "MACD", noOfDays)
        self.noOfDays = noOfDays

    def testBackData(self):
        startIndex = START_INDEX
        endIndex = END_INDEX
        #self.df.drop(self.df.index[range(28)], inplace=True)
        df = self.getDataFrame()
        macdLine = df["MACD Line"]
        signalLine = df["Signal Line"]
        macd = df["MACD Histogram"]
        close = df["Close"]

        flag = True
        if macdLine[startIndex] < 0:
            flag = False

        # Test b/w MACD line & centerline(0)
        for i in range(startIndex+1, macdLine.count() - endIndex):
            if macdLine[i-1] < 0:
                flag=False
            else:
                flag = True

            if flag:
                if macdLine[i] <= 0:
                    self.sellSignal(i)
                    flag = False
            else:
                if macdLine[i] >= 0:
                    self.buySignal(i)
                    flag = True
        
        print "====== Test result b/w MACD line & centerline ======"  
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

        # Test b/w MACD Line and Signal Line
        self.resetValue()
        flag = True
        if macdLine[startIndex] < signalLine[startIndex]:
            flag = False

        for i in range(startIndex+1, macdLine.count() - endIndex):
            if macdLine[startIndex] < signalLine[startIndex]:
                flag = False
            else:
                flag=True
            if flag:
                if macdLine[i] < signalLine[i]:
                    self.sellSignal(i)
                    flag = False
            else:
                if macdLine[i] > signalLine[i]:
                    self.buySignal(i)
                    flag = True
        
        print "\n\n"
        print "====== Test result b/w MACD line & Signal line ====="
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

    def __call__(self):
        startIndex = START_INDEX
        #self.df.drop(self.df.index[range(28)], inplace=True)
        df = self.getDataFrame()
        macdLine = df["MACD Line"]
        signalLine = df["Signal Line"]
        macd = df["MACD Histogram"]
        close = df["Close"]

        flag = True
        if macdLine[startIndex] < 0:
            flag = False

        # Test b/w MACD line & centerline(0)
        for i in range(startIndex+1, macdLine.count()):
            if flag:
                if macdLine[i] <= 0:
                    if (i == macdLine.count()-1):
                        subject = "Stock Alert | Level 0"
                        content = "Sell signal for " + self.symbol + ". LTP: " + str(close[i]) + "\nMACD Indicator"
                        SENDMAIL(subject, content)
                    flag = False
            else:
                if macdLine[i] >= 0:
                    if (i == macdLine.count()-1):
                        subject = "Stock Alert | Level 0"
                        content = "Buy signal for " + self.symbol + ". LTP: " + str(close[i]) + "\nMACD Indicator"
                        SENDMAIL(subject, content)
                    flag = True
        

        # Test b/w MACD Line and Signal Line
        self.resetValue()
        flag = True
        if macdLine[startIndex] < signalLine[startIndex]:
            flag = False

        for i in range(startIndex+1, macdLine.count()):
            if flag:
                if macdLine[i] < signalLine[i]:
                    if (i == macdLine.count()-1):
                        subject = "Stock Alert | Level 0"
                        content = "Sell signal for " + self.symbol + ". LTP: " + str(close[i]) + "\nMACD Indicator"
                        SENDMAIL(subject, content)
                    flag = False
            else:
                if macdLine[i] > signalLine[i]:
                    if (i == macdLine.count()-1):
                        subject = "Stock Alert | Level 0"
                        content = "Sell signal for " + self.symbol + ". LTP: " + str(close[i]) + "\nMACD Indicator"
                        SENDMAIL(subject, content)
                    flag = True
        
        print "\n\n"
        print "====== Test result b/w MACD line & Signal line ====="
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()

if __name__ == "__main__":

    macdTesting = kMACDIndicatorTesting("SBIN")
    macdTesting()
    