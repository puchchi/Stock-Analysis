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
        self.totBuyProfitPip = 0
        self.totSellProfitPip = 0
        self.buyClosedMissed = 0
        self.sellClosedMissed = 0
        self.totNightHoldingSell = 0
        self.totNightHoldingBuy = 0
        self.totPip = 0
        self.lastSignal = ""      # 1 for buy, 2 for sell
        self.lastPrice = 0

        # Creating storage dataframe to store buy/sell calls 
        self.signalTestFile = CSV_SINGAL_DATA_DIRECTORY + "Currency"+ signalName + SIGNAL_TEST_RESULT + CSV_INDICATOR_EXTENSTION
        if path.exists(self.signalTestFile):
            try:
                parser = lambda date: pd.datetime.strptime(date, '%d-%m-%Y %H:%M')
                self.storageDF = pd.read_csv(self.signalTestFile, parse_dates = [2], date_parser = parser, index_col=0)
                self.storageDF['Time'] = self.storageDF['Time'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M'))
            except Exception as e:
                print "Exception while reading signal test file"
                print e

        else:
            columnList = ["Symbol", "Time", "Signal", "Current Close"]
            for i in range(noOfDays):
                columnList.append("Open" + str(i+1))
                columnList.append("High" + str(i+1))
                columnList.append("Low" + str(i+1))
                columnList.append("Close" + str(i+1))

            self.storageDF = pd.DataFrame(columns=columnList)


        parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        self.df = pd.read_csv(self.filename, parse_dates = [0], date_parser = parser, index_col = "Time")

    def dumpTestData(self):
        self.storageDF['Time'] = pd.to_datetime(self.storageDF.Time)
        self.storageDF = self.storageDF.sort_values(by='Time', ascending=True)
        self.storageDF['Time'] = self.storageDF['Time'].apply(lambda x: x.strftime('%d-%m-%Y %H:%M'))
        self.storageDF.to_csv(self.signalTestFile)

        #self.perPassFailDF.to_csv(self.perPassFailFile)

    def getDataFrame(self):
        return self.df

    def sellSignal(self, index):
        date = datetime.strptime(str(self.df.index[index]), "%Y-%m-%d %H:%M:%S")
        lowerLimitDate = datetime.strptime(testDataDateLower, "%d-%b-%Y")
        upperLimitDate = datetime.strptime(testDataDateUpper, "%d-%b-%Y")
        if (date < lowerLimitDate or date > upperLimitDate):
            return

        minClose = min(self.df["Close"][index+1:index+self.noOfDays+1])
        minLow = min(self.df["Low"][index+1:index+self.noOfDays+1])
        print "--------------Sell Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Lows in nxt " + str(self.noOfDays) + " days : " + str(self.df["Low"][index+1:index+self.noOfDays+1])
                    
        # Reduce 1%

        if minClose < (self.df["Close"][index]*0.999):
            self.totSPass = self.totSPass + 1
        else:
            self.totSFail = self.totSFail + 1
            print "Failed======================================"

        if minLow < (self.df["Close"][index]*0.999):
            self.totSPassFromLow = self.totSPassFromLow + 1
        else:
            self.totSFailFromLow = self.totSFailFromLow + 1
            print "Failed======================================"

        # inserting signal in dataframe
        date = str(date.strftime("%d-%b-%Y %H:%M" ))
        storage = [self.symbol ,date, "Sell", self.df["Close"][index]]        

        try:
            for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
                storage.append(self.df["Open"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["High"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["Low"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["Close"][index+1:index+self.noOfDays+1][i])
       
            self.storageDF.loc[self.storageDF.shape[0]+1] = storage

            # Checking for threshold pip
            sellingPrice = self.df["Close"][index]
            stopLoss = sellingPrice + 0.0001*STOPLOSS_PIP
            targetPrice = sellingPrice - 0.0001*TARGET_PIP
            flag = True

            for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
                high = self.df["High"][index+1:index+self.noOfDays+1][i]
                low = self.df["Low"][index+1:index+self.noOfDays+1][i]
                if (high >= stopLoss):
                    self.totSellProfitPip-=STOPLOSS_PIP

                    currentDate = self.df.index[index+1:index+self.noOfDays+1][i]
                    buyingDate = self.df.index[index]
                    holdingNight = int((currentDate-buyingDate).days)
                    self.totNightHoldingSell+= holdingNight
                    flag=False
                    break
                elif (low <= targetPrice):
                    self.totSellProfitPip+=TARGET_PIP

                    currentDate = self.df.index[index+1:index+self.noOfDays+1][i]
                    buyingDate = self.df.index[index]
                    holdingNight = int((currentDate-buyingDate).days)
                    self.totNightHoldingSell+= holdingNight
                    flag=False
                    break

            # Going beyond set no of day
            if flag:
                dfLen = self.df["Open"].__len__()
                for i in range (index+self.noOfDays+1, dfLen):
                    high = self.df["High"][i]
                    low = self.df["Low"][i]
                    if (high >= stopLoss):
                        self.totSellProfitPip-=STOPLOSS_PIP

                        currentDate = self.df.index[i]
                        buyingDate = self.df.index[index]
                        holdingNight = int((currentDate-buyingDate).days)
                        self.totNightHoldingSell+= holdingNight
                        print "Extended target(SL) on " + str(self.df.index[i])
                        flag=False

                        break
                    elif (low <= targetPrice):
                        self.totSellProfitPip+=TARGET_PIP
                
                        currentDate = self.df.index[i]
                        buyingDate = self.df.index[index]
                        holdingNight = int((currentDate-buyingDate).days)
                        self.totNightHoldingSell+= holdingNight
                        flag=False
                        print "Extended target(TP) on " + str(self.df.index[i])
                        break

            if flag:
                self.sellClosedMissed+=1

        except Exception as e:
            print "Exception in SellSignal IndicatorTesterClass, as noOdDays are less"
            print e

        # calculating total pips earned/lost
        sellingPrice = self.df["Close"][index]
        deltaPip = self.lastPrice - sellingPrice
        if self.lastSignal == "Sell":
            self.totPip += (-1)*deltaPip
        if self.lastSignal == "Buy":
            self.totPip += deltaPip

        self.lastPrice = sellingPrice
        self.lastSignal = "Sell"

       

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

        # Reducing brokerage
        self.totSellProfitPip = self.totSellProfitPip - BROKERAGE_PIP* (self.totSPass + self.totSFail)
        print "Total profit pip in selling for threshold pip: " + str(TARGET_PIP) + " is : " + str(self.totSellProfitPip) 
        print "Sell Closed missed: " + str(self.sellClosedMissed)
        print "Total Night holding: " + str(self.totNightHoldingSell)
        print "Total Pip earned: " + str(self.totPip*1000)

    def buySignal(self, index):
        date = datetime.strptime(str(self.df.index[index]), "%Y-%m-%d %H:%M:%S")
        lowerLimitDate = datetime.strptime(testDataDateLower, "%d-%b-%Y")
        upperLimitDate = datetime.strptime(testDataDateUpper, "%d-%b-%Y")
        if (date < lowerLimitDate or date > upperLimitDate):
            return
        
        maxClose = max(self.df["Close"][index+1:index+self.noOfDays+1])
        maxHigh = max(self.df["High"][index+1:index+self.noOfDays+1])
        print "++++++++++++++Buy Signal : " + str(self.df.index[index]) + " Current Close : " + str(self.df["Close"][index]) + " Highs in nxt " + str(self.noOfDays) + " days : " + str(self.df["High"][index+1:index+self.noOfDays+1])
               
        # 1% hike

        if maxClose > (self.df["Close"][index]*1.001) :
            self.totBPass = self.totBPass + 1
        else:
            self.totBFail = self.totBFail + 1
            print "Failed======================================"
        if maxHigh > (self.df["Close"][index]*1.001):
            self.totBPassFromHigh = self.totBPassFromHigh + 1
        else:
            self.totBFailFromHigh = self.totBFailFromHigh + 1
            print "Failed======================================"
        
        # inserting signal in dataframe
        date = str(date.strftime("%d-%b-%Y"))
        storage = [self.symbol ,date, "Buy", self.df["Close"][index]]

        try:
            for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
                storage.append(self.df["Open"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["High"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["Low"][index+1:index+self.noOfDays+1][i])
                storage.append(self.df["Close"][index+1:index+self.noOfDays+1][i])
       
            #print str(self.storageDF)
            #print str(storage)
            self.storageDF.loc[self.storageDF.shape[0]+1] = storage

            # Checking for threshold pip
            buyingPrice = self.df["Close"][index]
            stopLoss = buyingPrice - 0.0001*STOPLOSS_PIP
            targetPrice = buyingPrice + 0.0001*TARGET_PIP
            flag=True
            for i in range (self.df["Open"][index+1:index+self.noOfDays+1].__len__()):
                high = self.df["High"][index+1:index+self.noOfDays+1][i]
                low = self.df["Low"][index+1:index+self.noOfDays+1][i]
                if (low <= stopLoss):
                    self.totBuyProfitPip-=STOPLOSS_PIP
                    currentDate = self.df.index[index+1:index+self.noOfDays+1][i]
                    buyingDate = self.df.index[index]
                    holdingNight = int((currentDate-buyingDate).days)
                    self.totNightHoldingBuy+= holdingNight
                    flag=False
                    break
                elif (high >= targetPrice):
                    self.totBuyProfitPip+=TARGET_PIP

                    currentDate = self.df.index[index+1:index+self.noOfDays+1][i]
                    buyingDate = self.df.index[index]
                    holdingNight = int((currentDate-buyingDate).days)
                    self.totNightHoldingBuy+= holdingNight
                    flag=False
                    break

            # Going beyond set no of day
            if flag:
                dfLen = self.df["Open"].__len__()
                for i in range (index+self.noOfDays+1, dfLen):
                    high = self.df["High"][i]
                    low = self.df["Low"][i]
                    if (low <= stopLoss):
                        self.totBuyProfitPip-=STOPLOSS_PIP
                    
                        currentDate = self.df.index[i]
                        buyingDate = self.df.index[index]
                        holdingNight = int((currentDate-buyingDate).days)
                        self.totNightHoldingSell+= holdingNight
                        flag=False
                        print "Extended Close(SL) on "+ str(self.df.index[i])
                        break
                    elif (high >= targetPrice):
                        self.totBuyProfitPip+=TARGET_PIP

                        currentDate = self.df.index[i]
                        buyingDate = self.df.index[index]
                        holdingNight = int((currentDate-buyingDate).days)
                        flag=False
                        print "Extended Close(TP) on "+ str(self.df.index[i])
                        break

            if flag:
                self.buyClosedMissed+=1
        except Exception as e:
            print "Exception in BuySignal IndicatorTesterClass, as noOdDays are less"
            print e

        # calculating total pips earned/lost
        buyPrice = self.df["Close"][index]
        deltaPip = self.lastPrice - buyPrice
        if self.lastSignal == "Sell":
            self.totPip += (+1)*deltaPip
        if self.lastSignal == "Buy":
            self.totPip += (-1)*deltaPip

        self.lastPrice = buyPrice
        self.lastSignal = "Buy"

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

        # Reducing brokerage
        self.totBuyProfitPip = self.totBuyProfitPip - BROKERAGE_PIP*(self.totBPass + self.totBFail)
        print "Total profit pip in buying for threshold pip: " + str(TARGET_PIP) + " is : " + str(self.totBuyProfitPip) 
        print "Buy Closed missed: " + str(self.buyClosedMissed)
        print "Total Night holding: " + str(self.totNightHoldingBuy)
        print "Total Pip earned: " + str(self.totPip*1000)

    def resetValue(self):
        self.totBPass = 0
        self.totBFail = 0
        self.totBPassFromHigh = 0
        self.totBFailFromHigh = 0
        self.totSPass = 0
        self.totSFail = 0
        self.totSPassFromLow = 0
        self.totSFailFromLow = 0