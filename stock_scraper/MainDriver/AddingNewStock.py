# This file will do following steps.
# 1: Initialize db by creating table for given stock if it not present there.
# 2: Scrape data of that stock and fill in db.
# 3: Create CSV file from db.
# 4: Create all Indicators and save them in another CSV file.
# 5: Test Indicator 

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import pandas as pd
from DBInitialize import Initialize
from scraper import utility, HistoricEquity, HistoricIndex, HistoricOption, LiveOption
from MainDriver import ComputeIndicators, OptionRelatedTesting
from MainDriver.CSVCreator import CreateSpotCSVDataFile, CreateOptionCSVDataFile
from MainDriver.IndicatorTester import ADXIndicatorTesting, MACDIndicatorTesting, CommonSignalChecker

class kAddingNewStock:

    def __init__(self, stockName):
        self.stockName = stockName
        self.stockType = utility.stockType
        self.dbTableName = utility.dbTableName
        self.dbTableNameOption = utility.dbTableNameOption
        self.startYear = utility.startYear
        self.endYear = utility.endYear
        self.dbStartDate = utility.dbStartDate
        self.dbEndDate = utility.dbEndDate
        self.csvFileName = utility.csvFileName
        self.csvFileNameOption = utility.csvFileNameOption
        self.csvFileNameWithIndicators = utility.csvFileNameWithIndicators
        self.expiries = utility.expiries
        self.instrumentType = utility.instrumentType
        self.expiry = ""

    def __call__(self):
        self.callInternal()
        
    def callInternal(self):

        # 1: Initialize db by creating table for given stock if it not present there.
        self.initializeDb()

        # 2: Scrape spot data of that stock and fill in db.
        self.scrapeSpotData()

        # 3: Create CSV file from db.
        self.createCSVFile()

        # 4: Create all Indicators and save them in another CSV file.
        self.createIndicators()

        # 5: Test Indicator 
        self.testIndicator()

    def initializeDb(self):
        print "==============================================="
        print "Creating database table for :" + self.stockName

        if self.stockType == "Index" or self.stockType == "Equity":
            dbInitialize = Initialize.kInitialize(self.dbTableName)
            dbInitialize()
        elif self.stockType == "Option":
            for expiry in self.expiries:
                tableName = self.dbTableNameOption + expiry
                dbInitialize = Initialize.kInitialize(self.dbTableNameOption)
                dbInitialize()
        elif self.stockType == "LiveOption":
            dbInitialize = Initialize.kInitialize(utility.dbTableNameLiveOption)
            dbInitialize()

    def scrapeSpotData(self):
        print "==============================================="
        print "Scraping data from NSE :"

        if self.stockType == "Index":
            autoSpotValue = HistoricIndex.kHistoricIndex(self.stockName, utility.dateDecoding(self.dbStartDate), utility.dateDecoding(self.dbEndDate), utility.HISTORIC_STOCK_TABLENAME)
            autoSpotValue()
        elif self.stockType == "Equity":
            autoSpotValue = HistoricEquity.kHistoricEquity(self.stockName, utility.dateDecoding(self.dbStartDate), utility.dateDecoding(self.dbEndDate), utility.HISTORIC_STOCK_TABLENAME)
            autoSpotValue()
        elif self.stockType == "Option":
            autoOptionValue = HistoricOption.kHistoricOption(self.stockName, self.expiries, self.instrumentType)
            autoOptionValue()
        elif self.stockType == "LiveOption":
            autoLiveOptionValue = LiveOption.kLiveOption(self.stockName)
            #infiniteRunningTask = InfiniteRunningTask.kInfiniteRunningTask(autoLiveOptionValue, 2300, 2320, True, self.stockName)
            #infiniteRunningTask.do()
            autoLiveOptionValue()

    def createCSVFile(self):
        print "==============================================="
        print "Creating CSV file for :" + self.stockName

        if self.stockType == "Index" or self.stockType == "Equity":
            createCSVFile = CreateSpotCSVDataFile.kCreateSpotCSVDataFile(self.stockName, utility.dateDecoding(self.dbStartDate), utility.dateDecoding(self.dbEndDate))
        elif self.stockType == "Option":
            tableNames = []
            fileNames = []
            for expiry in self.expiries:
                tableNames.append(self.dbTableNameOption + expiry)
                fileNames.append(self.csvFileNameOption + expiry + ".CSV")
            createCSVFile = CreateOptionCSVDataFile.kCreateOptionCSVDataFile(self.stockName, fileNames)
        createCSVFile()

    def createIndicators(self):
        
        print "==============================================="
        print "Creating indicator's CSV file for :" + self.stockName
        if self.stockType == "Index" or self.stockType == "Equity":
            computeIndicator = ComputeIndicators.kComputeIndicators(self.stockName)
            computeIndicator()
        elif self.stockType == "Currency":
            computeIndicator = ComputeIndicators.kComputeIndicators(self.stockName)
            computeIndicator.calculateADX()

    def testIndicator(self):
        print "==============================================="
        print "Testing indicator for :" + self.stockName
        try:
            if self.stockType == "Index" or self.stockType == "Equity":
                adxTestIndicator = ADXIndicatorTesting.kADXIndicatorTesting(self.stockName, 4)
                adxTestIndicator.testBackData()
                adxTestIndicator.dumpTestData()
                #testIndicator()

                macdTestIndicator = MACDIndicatorTesting.kMACDIndicatorTesting(self.stockName, 4)
                macdTestIndicator.testBackData()
                macdTestIndicator.dumpTestData()
                #macdTestIndicator()
            elif self.stockType == "Option":
                optionTesting = OptionRelatedTesting.kOptionRelatedTesting(utility.optionCSVFileForTesting)
                optionTesting()
            elif self.stockType == "Currency":
                adxTestIndicator = ADXIndicatorTesting.kADXIndicatorTesting(self.stockName, 4)
                adxTestIndicator.testBackData()
                adxTestIndicator.dumpTestData()

        except Exception as e:
            print "Exeception in testing indicator."
            print e

if __name__ == "__main__":

    for stock in utility.stockList:

        #addingNewStock = kAddingNewStock(utility.stockName)
        addingNewStock = kAddingNewStock(stock)
        # if you want to do all 5 steps, uncomment following line
        #addingNewStock()

        #addingNewStock.initializeDb()
        #addingNewStock.scrapeSpotData()
        #addingNewStock.createCSVFile()
        #addingNewStock.createIndicators()
        addingNewStock.testIndicator()

    # Checking for common signal in ADX & MACD
    #testerObj = CommonSignalChecker.kCommonSignalChecker(["ADX", "MACD"])
    #testerObj()
