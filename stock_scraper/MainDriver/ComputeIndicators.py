import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import pandas as pd
from Indicators import AccumulationNDistributionLine, OnBalanceVolume, AverageDirectionalIndex, MACD, RSI
from scraper.utility import *
from numpy import nan

class kComputeIndicators:
    def __init__(self, symbol):
        self.symbol = symbol
        self.csvFileName = CSV_DATA_DIRECTORY + symbol + CSV_EXTENSION
        self.csvFileNameWithIndicators = CSV_DATA_DIRECTORY + symbol + CSV_INDICATOR_EXTENSTION

        try:
            #parser = lambda date: pd.datetime.strptime(date, '%d.%m.%Y %H:%M:%S.%f')
            parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d %H:%M')
            self.df = pd.read_csv(self.csvFileName, parse_dates = [0], date_parser = parser, index_col = "Time")
        
        except Exception as e:
            print " Exception in reading csv file in compute indicator init()"
            print e
        

    def __call__(self):
        dataframe = self.df

        # cleaing dataframe for any record which has volume 0
        dataframe= dataframe.replace(0,nan)
        dataframe= dataframe.dropna(how='any',axis=0)

        # Calculating ADL
        adl = AccumulationNDistributionLine.kAccumulationNDistributionLine()
        adlSeries = adl.calculate(dataframe)
        adlDataframe = pd.DataFrame(adlSeries, columns=["ADL"])

        # Calculating OBV
        obv = OnBalanceVolume.kOnBalanceVolume()
        obvSeries = obv.calculate(dataframe)
        obvDataframe = pd.DataFrame(obvSeries, columns=["OBV"])

        # Calculating ADX
        adx = AverageDirectionalIndex.kAverageDirectionalIndex()
        adxDataframe = adx.calculate(dataframe)

        # Calculating MACD
        macd = MACD.kMACD()
        macdDataframe = macd.Calculate(dataframe)

        # Calculating RSI
        rsi = RSI.kRSI()
        rsiSeries = rsi.Calculate(dataframe)
        rsiDataframe = pd.DataFrame(rsiSeries, columns=["RSI"])

        dataframe = dataframe.merge(adlDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(obvDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(adxDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(macdDataframe, left_index=True, right_index=True)
        dataframe = dataframe.merge(rsiDataframe, left_index=True, right_index=True)

        dataframe.to_csv(self.csvFileNameWithIndicators)

    def calculateADX(self):
        dataframe = self.df

        # for eurusd we going to need date b/w 2016-1-1 to 2016-12-31
        #remove this part
        dataframe = dataframe.loc['2016-01-01':'2016-12-31']

        # cleaing dataframe for any record which has volume 0
        dataframe= dataframe.replace(0,nan)
        dataframe= dataframe.dropna(how='any',axis=0)

        # Calculating ADX
        adx = AverageDirectionalIndex.kAverageDirectionalIndex()
        adxDataframe = adx.calculate(dataframe)

        dataframe = dataframe.merge(adxDataframe, left_index=True, right_index=True)

        dataframe.to_csv(self.csvFileNameWithIndicators)

class kCommand:

    def __init__(self, *args):
        self.args = args

    def run_job(self, queue, args):
        try:
            computeIndicator = kComputeIndicators(symbol=self.args[0][0])
            computeIndicator()
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
        return "Compute indicator command"

if __name__ == "__main__":

    computeIndicator = kComputeIndicators("SBIN")
    dataframe = computeIndicator()

