import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )

import pandas as pd
from scraper.utility import *
from MainDriver.IndicatorTester.IndicatorTesterClass import kIndicatorTesterClass
from multiprocessing import Process, Queue

class kADXIndicatorTesting(kIndicatorTesterClass):

    def __init__(self, symbol, noOfDays=3):
        self.symbol = symbol
        self.filename = CSV_DATA_DIRECTORY + symbol + CSV_INDICATOR_EXTENSTION
        kIndicatorTesterClass.__init__(self, self.symbol, "ADX", noOfDays)
        self.noOfDays = noOfDays

    # Use this to test effeciency of this indicator
    def testBackData(self):
        startIndex = START_INDEX
        endIndex = END_INDEX
        df = self.getDataFrame()
        #self.df.drop(self.df.index[range(28)], inplace=True)
        plusDIs = df["+DI14"]
        minusDIs = df["-DI14"]
        adxs = df["ADX"]
        close = df["Close"]

        flag = True
        if minusDIs[startIndex] > plusDIs[startIndex]:
            flag = False

        for i in range(startIndex + 1, plusDIs.count() - endIndex):
            if minusDIs[i-1] > plusDIs[i-1]:
                flag = False
            else:
                flag = True

            if flag:
                if minusDIs[i] > plusDIs[i] and adxs[i] > 20:
                    #print "plusDI: "+ str(plusDIs[i]) + " minusDI: " + str(minusDIs[i]) + " adx: " + str(adxs[i])
                    self.sellSignal(i)
                    flag = False
            else:
                if plusDIs[i] > minusDIs[i] and adxs[i] > 20:
                    #print "plusDI: "+ str(plusDIs[i]) + " minusDI: " + str(minusDIs[i]) + " adx: " + str(adxs[i])
                    self.buySignal(i)
                    flag = True
            
        print "====== Test result b/w +DI14 & -DI14 having ADX>20 ======"
        self.buySignalResult()
        print "===================================="
        self.sellSignalResult()


    def __call__(self):
        startIndex = START_INDEX
        df = self.getDataFrame()
        #self.df.drop(self.df.index[range(28)], inplace=True)
        plusDIs = df["+DI14"]
        minusDIs = df["-DI14"]
        adxs = df["ADX"]
        close = df["Close"]

        flag = True
            
        lastIndex = plusDIs.count()-1
        if (minusDIs[lastIndex-1] > plusDIs[lastIndex-1]):
            flag = False
        else:
            flag = True

        if flag:
            if minusDIs[lastIndex] > plusDIs[lastIndex] and adxs[lastIndex] > 20:
                ltp = close[lastIndex]
                tp1 = ltp*(1-TARGET_PRICE_1*0.01)
                tp2 = ltp*(1-TARGET_PRICE_2*0.01)
                tp3 = ltp*(1-TARGET_PRICE_3*0.01)
                sl = ltp*(1+STOP_LOSS*0.01)
                
                subject = "Stock Alert | Date " + str(df.index[lastIndex])
                content = "Sell signal for " + self.symbol + ". LTP: " + str(close[lastIndex])
                content += "\n\tTarget prices: " + str(tp1) + ", " + str(tp2) + ", " + str(tp3)
                content += "\n\tStoploss: " + str(sl)
                content += "\n\nADX Indicator"
                SENDMAIL(subject, content)
                print "\n\n\n###########################    Sell signal " + self.symbol + " on " + str(df.index[lastIndex]) + ": LTP " + str(close[lastIndex]) + "Target prices: " + str(tp1) + ", " + str(tp2) + ", " + str(tp3) + "Stoploss: " + str(sl) + "     ###########################\n\n\n"
            else:
                print "No Sell signal for " + self.symbol + " on " + str(df.index[lastIndex])
        else:
            if plusDIs[lastIndex] > minusDIs[lastIndex] and adxs[lastIndex] > 20:
                ltp = close[lastIndex]
                tp1 = ltp*(1+TARGET_PRICE_1*0.01)
                tp2 = ltp*(1+TARGET_PRICE_2*0.01)
                tp3 = ltp*(1+TARGET_PRICE_3*0.01)
                sl = ltp*(1-STOP_LOSS*0.01)
                subject = "Stock Alert | Date " + str(df.index[lastIndex])
                content = "Buy signal for " + self.symbol + ". LTP: " + str(close[lastIndex])
                content += "\n\tTarget prices: " + str(tp1) + ", " + str(tp2) + ", " + str(tp3)
                content += "\n\tStoploss: " + str(sl)
                content += "\n\nADX Indicator"

                SENDMAIL(subject, content)
                print "\n\n\n###########################   Buy Signal for " + self.symbol + " on " + str(df.index[lastIndex]) + ": LTP " + str(close[lastIndex]) + "Target prices: " + str(tp1) + ", " + str(tp2) + ", " + str(tp3) + "Stoploss: " + str(sl) +"    ###########################\n\n\n"
            else:
                print "No Buy signal for " + self.symbol + " on " + str(df.index[lastIndex])

class kCommand:

    def __init__(self, *args):
        self.args = args

    def run_job(self, queue, args):
        try:
            adxIndicatorTesting = kADXIndicatorTesting(symbol=self.args[0][0])
            adxIndicatorTesting()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    def do(self):

        queue = Queue()
        process = Process(target=self.run_job, args=(queue, self.args))
        process.start()
        result = queue.get()
        process.join()

        if result is not None:
            raise result

    def get_name(self):
        return "ADX indicator testing command"

if __name__ == "__main__":

    adxTesting = kADXIndicatorTesting("SBIN", 3)
    #adxTesting.testBackData()
    adxTesting()
    