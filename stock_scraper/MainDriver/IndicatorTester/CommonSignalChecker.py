import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd
from scraper.utility import *
from datetime import datetime

class kCommonSignalChecker:

    def __init__(self, signalList):
        self.signalList =  signalList

        # Creating storage dataframe to store buy/sell calls 
        self.signalTestFile = []
        self.signalTestFile.append(CSV_DATA_DIRECTORY + self.signalList[0] + SIGNAL_TEST_RESULT + CSV_INDICATOR_EXTENSTION)
        self.signalTestFile.append(CSV_DATA_DIRECTORY + self.signalList[1] + SIGNAL_TEST_RESULT + CSV_INDICATOR_EXTENSTION)

        try:
            parser = lambda date: pd.datetime.strptime(date, '%d-%b-%Y')
            self.storageDF1 = pd.read_csv(self.signalTestFile[0], parse_dates = [2], date_parser = parser, index_col=0)
            self.storageDF1['Date'] = self.storageDF1['Date'].apply(lambda x: x.strftime('%d-%b-%Y'))

            self.storageDF2 = pd.read_csv(self.signalTestFile[1], parse_dates = [2], date_parser = parser, index_col=0)
            self.storageDF2['Date'] = self.storageDF2['Date'].apply(lambda x: x.strftime('%d-%b-%Y'))
        except Exception as e:
            print "Exception while reading signal test file"
            print e

    def __call__(self):

        for i in range(self.storageDF1['Date'].__len__()):
            date1 = self.storageDF1['Date'][i+1]
            stockName1 = self.storageDF1['Symbol'][i+1]
            for j in range(self.storageDF2['Date'].__len__()):
                date2 = self.storageDF2['Date'][j+1]
                stockName2 = self.storageDF2['Symbol'][j+1]

                if (date1 == date2 and stockName1 == stockName2):
                    print "Date:" + date1 + " Symbol: " + stockName1
                    #print self.storageDF2[j]
