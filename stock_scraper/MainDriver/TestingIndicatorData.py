import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import pandas as pd

class kTestingIndicatorData:
    def __init__(self, filename):
        parser = lambda date: pd.datetime.strptime(date, '%Y-%m-%d')
        self.df = pd.read_csv(filename, parse_dates = [0], date_parser = parser, index_col = "Date")

    def CompileIndicators(self, delRows=0, delCols=[], trainingRows=0, trainingPer=0, trainingDataFName="", testingDataFName=""):

        prevClose = pd.Series({0:0})
        for i in range(self.df["Close"].count()-1):
            prevClose = prevClose.append(pd.Series({i+1:self.df["Close"][i]}))

        prevCloseDF = pd.DataFrame(prevClose, columns=["Previous Close"])
        prevCloseDF.index = self.df.index
        self.df = self.df.merge(prevCloseDF, left_index=True, right_index=True)

        if delRows > 0:
            self.df.drop(self.df.index[range(delRows)], inplace=True)

        if delCols.__len__() > 0:
            self.df.drop(delCols, axis=1, inplace=True)

        trainingDF = pd.DataFrame()
        testingDF = pd.DataFrame()
        
        if trainingRows > 0:
            trainingDF = self.df[:trainingRows]
            testingDF = self.df[trainingRows+1:].copy()

        elif trainingPer > 0:
            totalRows = len(self.df.index)
            trainingPerRows = int(totalRows * trainingPer / 100);
            trainingDF = self.df[:trainingPerRows]
            testingDF = self.df[trainingPerRows+1:].copy()

        if len(trainingDataFName) > 0:
            trainingDF.to_csv(trainingDataFName)

        # Removing Close from testing data
        testingDF.drop("Close", axis=1, inplace=True)
        if len(testingDataFName) > 0:
            testingDF.to_csv(testingDataFName)


if __name__ == "__main__":

    testing = kTestingIndicatorData("data/niftyWithIndicatorsOriginal.csv")
    testing.CompileIndicators(delRows=28, delCols=["Open", "High", "Low", "Volume", "+DI14", "-DI14","Signal Line", "MACD Histogram"], trainingRows=1500, 
                                          trainingDataFName="data/niftyTrainingData.csv", testingDataFName="data/niftyTestingData.csv")
