import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.abspath(__file__) ) )

from scraper import LiveOption, HistoricOption, LiveIndex, LiveEquity, HistoricIndex, HistoricEquity
from DBInitialize import CleanNCreateLiveOptionDB, CleanNCreateLiveStockDB
from CSVCreator import CreateSpotCSVDataFile
from MainDriver import ComputeIndicators
from MainDriver.IndicatorTester import ADXIndicatorTesting
from scraper.utility import *

# Date format from here: 01-Jan-2018

SCHEDULED_TASK=(
    #(Module, expected arugument, ((from(HHMM), to(HHMM), timedelta(in minute)) or (when(HHMM))))
    # argument (symbol/list of symbol, [args], type, tableName)

     # Clean DB( we wil create only live option table each time, historic table will be made one time only)
    (CleanNCreateLiveOptionDB, [], ["0800"], ),
    (CleanNCreateLiveStockDB, [], ["0800"], ),

    # live option
    #(LiveOption, ["Nifty", CURRENT_EXPIRY, "OPTIDX", LIVE_OPTION_TABLENAME], ["0900", "1600", 10], ),
    #(LiveOption, ["BankNifty", CURRENT_EXPIRY, "OPTIDX", LIVE_OPTION_TABLENAME], ["0900", "1600", 10], ),

    # live index
    #(LiveIndex, ["NIFTY", LIVE_STOCK_TABLENAME], ["0900", "1600", 10],),
    #(LiveIndex, ["BANKNIFTY", LIVE_STOCK_TABLENAME], ["0900", "1600", 10],),

    # live equity
    (LiveEquity, [NIFTY_STOCK_LIST, LIVE_STOCK_TABLENAME], ["0900", "1600", 10],),
    #(LiveEquity, ["HDFC", LIVE_STOCK_TABLENAME], ["0900", "1600", 1],),

    # historic option
    #(HistoricOption, ["SBIN", CURRENT_EXPIRY, "OPTSTK", HISTORIC_OPTION_TABLENAME], ["0800"], ),
    #(HistoricOption, ["Nifty", CURRENT_EXPIRY, "OPTIDX", HISTORIC_OPTION_TABLENAME], ["0800"], ),
    #(HistoricOption, ["BankNifty", CURRENT_EXPIRY, "OPTIDX", HISTORIC_OPTION_TABLENAME], ["0800"], ),

    # historic Index 
    #(HistoricIndex, ["NIFTY", HISTORIC_START_DATE, CURRENT_DATE, HISTORIC_STOCK_TABLENAME], ["0800"], ),
    #(HistoricIndex, ["BANKNIFTY", HISTORIC_START_DATE, CURRENT_DATE, HISTORIC_STOCK_TABLENAME], ["0800"], ),

    # historic Equity 
    (HistoricEquity, [NIFTY_STOCK_LIST, HISTORIC_START_DATE, CURRENT_DATE, HISTORIC_STOCK_TABLENAME], ["0800"], ),

    # Creating CSV for stock(Index/Equity), NOTE: It will create indicator csv too
    (CreateSpotCSVDataFile, [NIFTY_STOCK_LIST, INDICATOR_START_DATE], ["1200", "1520", 10],),

    # Testing ADX indicator for Nifty stocks(true is placeholder arg)
    (ADXIndicatorTesting, [NIFTY_STOCK_LIST, True], ["1200", "1525", 10],),
    )
