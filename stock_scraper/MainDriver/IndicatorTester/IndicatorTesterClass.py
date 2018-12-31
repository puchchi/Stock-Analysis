import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from scraper.utility import *
from datetime import datetime

class kIndicatorTesterClass:

    def __init__(self, symbol, signalName, noOfDays=3):
        self.filename =  self.filename = CSV_DATA_DIRECTORY + symbol + CSV_INDICATOR_EXTENSTION
        self.signalName = signalName
        self.noOfDays = noOfDays
        self.totBPass = 0
        self.totBFail = 0
        self.totBPassFromHigh = 0
        self.totBFailFromHigh = 0
        self.totSPass = 0
        self.totSFail = 0
        self.totSPassFromLow = 0
        self.totSFailFromLow = 0
        self.symbol = symbol

        # Creating storage dataframe to store buy/sell calls 
        self.signalTestFile = CSV_SINGAL_DATA_DIRECTORY + signalName + SIGNAL_TEST_RESULT + CSV_INDICATOR_EXTENSTION
        if path.exists(self.signalTestFile):
            try:
                parser = lambda date: pd.datetime.strptime(date, '%d-%b-%Y')
                self.storageDF = pd.read_csv(self.signalTestFile, parse_dates = [2], date_parser = parser, index_col=0)
                self.storageDF['Date'] = self.storageDF['Date'].apply(lambda x: x.strftime('%d-%b-%Y'))
            except Exception as e:
                print "Exception while reading signal test file"
                print e

        else:
            columnList = ["Symbol", "Date", "Signal", "Current Close"]
            for i in range(noOfDays):
                columnList.append("Open" + str(i+1))
                columnList.append("High" + str(i+1))
                columnList.append("Low" + str(i+1))
                columnList.append("Close" + str(i+1))

            self.storageDF = pd.DataFrame(columns=columnList)

        # creating percentage dataframe
        self.perPassFailFile = CSV_SINGAL_DATA_DIRECTORY + signalName + "PercentagePassFail" + CSV_INDICATOR_EXTENSTION
        if path.exists(self.perPassFailFile):
            try:
                self.perPassFailDF = pd.read_csv(self.perPassFailFile, index_col=0)
            except Exception as e:
                print "Exception while reading signal test file"
                print e

        else:
            columnList = ["Symbol", "Type", "total Sample", "Normal %", "From Upper/Lower %"]
            self.perPassFailDF = pd.DataFrame(columns=columnList)

        parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d')
        self.df = pd.read_csv(self.filename, parse_dates = [0], date_parser = parser, index_col = "Date")

    def dumpTestData(self):
        self.storageDF['Date'] = pd.to_datetime(self.storageDF.Date)
        self.storageDF = self.storageDF.sort_values(by='Date', ascending=True)
        self.storageDF['Date'] = self.storageDF['Date'].apply(lambda x: x.strftime('%d-%b-%Y'))
        self.storageDF.to_csv(self.signalTestFile)

        #self.perPassFailDF.to_csv(self.perPassFailFile)

    def getDataFrame(self):
        return self.df

    def sellSignal(self, index):
        date = datetime.strptime(str(self.df.index[index]), "%Y-%m-%d %H:%M:%S")
        lowerLimitDate = datetime.strptime(testDataDateLower, "%d-%b-%Y")
        if (date < lowerLimitDate):
            return
        
        for i in range(self.perPassFailDF["Symbol"].__len__()):
            if self.perPassFailDF["Symbol"][i+1] == self.symbol and str(self.perPassFailDF["Type"][i+1])=="Sell":
                if self.perPassFailDF["Normal %"][i+1] < thresholdPassFailPer:
                    return
                else:
                    break

        minClose = min(self.df["Close"][index+1:index+self.noOfDays+1])
        minLow = min(self.df["Low"][index+1:index+self.noOfDays+1])
        print "--------------Sell Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Lows in nxt " + str(self.noOfDays) + " days : " + str(self.df["Low"][index+1:index+self.noOfDays+1])
                    
        if minClose < self.df["Close"][index]:
            self.totSPass = self.totSPass + 1
        else:
            self.totSFail = self.totSFail + 1

        if minLow < self.df["Close"][index]:
            self.totSPassFromLow = self.totSPassFromLow + 1
        else:
            self.totSFailFromLow = self.totSFailFromLow + 1

        # inserting signal in dataframe
        date = str(date.strftime("%d-%b-%Y"))
        storage = [self.symbol ,date, "Sell", self.df["Close"][index]]        

        for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
            storage.append(self.df["Open"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["High"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["Low"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["Close"][index+1:index+self.noOfDays+1][i])
       
        self.storageDF.loc[self.storageDF.shape[0]+1] = storage

        # Special case
        #if minClose > self.df["Close"][index] and minLow < self.df["Close"][index]:
        #    print "--------------Sell Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + "Min Close in nxt " + str(self.noOfDays) + " days : " + str(self.df["Low"][index:index+self.noOfDays+1])

    def sellSignalResult(self):
        print "Total sell pass : " + str(self.totSPass)
        print "Total sell fail : " + str(self.totSFail)
        per = 0
        if ((self.totSPass + self.totSFail)!=0):
            per = float(self.totSPass)/(self.totSPass + self.totSFail)*100
        print "Total sell pass percentage in nxt " + str(self.noOfDays) + " days : " + str(per)

        print "Total sell pass from low: " + str(self.totSPassFromLow)
        print "Total sell fail from low: " + str(self.totSFailFromLow)
        perFromLow = 0
        if ((self.totSPassFromLow + self.totSFailFromLow)!=0):
            perFromLow = float(self.totSPassFromLow)/(self.totSPassFromLow + self.totSFailFromLow)*100
        print "Total sell pass percentage from low in nxt " + str(self.noOfDays) + " days : " + str(perFromLow)

        tempList = [self.symbol, "Sell",self.totSPass+self.totSFail, int(per), int(perFromLow)]
        self.perPassFailDF.loc[self.perPassFailDF.shape[0]+1] = tempList

    def buySignal(self, index):
        date = datetime.strptime(str(self.df.index[index]), "%Y-%m-%d %H:%M:%S")
        lowerLimitDate = datetime.strptime(testDataDateLower, "%d-%b-%Y")
        if (date < lowerLimitDate):
            return
        
        for i in range(self.perPassFailDF["Symbol"].__len__()):
            if self.perPassFailDF["Symbol"][i+1] == self.symbol and str(self.perPassFailDF["Type"][i+1])=="Buy":
                if self.perPassFailDF["Normal %"][i+1] < thresholdPassFailPer:
                    return
                else:
                    break
        

        maxClose = max(self.df["Close"][index+1:index+self.noOfDays+1])
        maxHigh = max(self.df["High"][index+1:index+self.noOfDays+1])
        print "++++++++++++++Buy Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Highs in nxt " + str(self.noOfDays) + " days : " + str(self.df["High"][index+1:index+self.noOfDays+1])
                    
        if maxClose > self.df["Close"][index]:
            self.totBPass = self.totBPass + 1
        else:
            self.totBFail = self.totBFail + 1
        if maxHigh > self.df["Close"][index]:
            self.totBPassFromHigh = self.totBPassFromHigh + 1
        else:
            self.totBFailFromHigh = self.totBFailFromHigh + 1
        
        # inserting signal in dataframe
        date = str(date.strftime("%d-%b-%Y"))
        storage = [self.symbol ,date, "Buy", self.df["Close"][index]]

        for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
            storage.append(self.df["Open"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["High"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["Low"][index+1:index+self.noOfDays+1][i])
            storage.append(self.df["Close"][index+1:index+self.noOfDays+1][i])
       
        #print str(self.storageDF)
        #print str(storage)
        self.storageDF.loc[self.storageDF.shape[0]+1] = storage

        # Special case
        #if maxClose < self.df["Close"][index] and maxHigh > self.df["Close"][index]:
        #    print "++++++++++++++Buy Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + "Max Close in nxt " + str(self.noOfDays) + " days : " + str(self.df["High"][index:index+self.noOfDays+1])

    def buySignalResult(self):
        print "Total buy pass : " + str(self.totBPass)
        print "Total buy fail : " + str(self.totBFail)
        per = 0
        if ((self.totBPass + self.totBFail)!=0):
            per = float(self.totBPass)/(self.totBPass + self.totBFail)*100
        print "Total buy pass percentage in nxt " + str(self.noOfDays) + " days : " + str(per)

        print "Total buy pass from high: " + str(self.totBPassFromHigh)
        print "Total buy fail from high: " + str(self.totBFailFromHigh)
        perFromHigh = 0
        if ((self.totBPassFromHigh + self.totBFailFromHigh)!=0):
            perFromHigh = float(self.totBPassFromHigh)/(self.totBPassFromHigh + self.totBFailFromHigh)*100
        print "Total buy pass percentage from high in nxt " + str(self.noOfDays) + " days : " + str(perFromHigh)

        tempList = [self.symbol, "Buy",self.totBPass+self.totBFail, int(per), int(perFromHigh)]
        self.perPassFailDF.loc[self.perPassFailDF.shape[0]+1] = tempList

    def resetValue(self):
        self.totBPass = 0
        self.totBFail = 0
        self.totBPassFromHigh = 0
        self.totBFailFromHigh = 0
        self.totSPass = 0
        self.totSFail = 0
        self.totSPassFromLow = 0
        self.totSFailFromLow = 0

