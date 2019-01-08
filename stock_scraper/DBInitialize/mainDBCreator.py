# It will read from scheduling and create tables needed accordingly

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
from scraper import utility
from MainDriver.scheduling import *


class kMainDBCreator():

    def __init__(self):
        self.tableNameToTypeSet = {}
        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
				            utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
            # Cursor will used in executing SQL query
            self.cursor = self.db.cursor()
        except Exception as e:
            print e
            print "Error in connecting Mysql db in mainDBCreator.py"


    def __call__(self):
        self.GetTableName()
        self.CreateTables()


    def GetTableName(self):

        for task in SCHEDULED_TASK:

            if (task[1].__len__() < 3):
                continue

            symbol = task[1][0]
            expiries = task[1][1]
            tableName = task[1][-1]

            if (tableName == utility.LIVE_OPTION_TABLENAME):
                self.tableNameToTypeSet.update({LIVE_OPTION_TABLENAME : "kLiveOption"})

            elif (tableName == utility.HISTORIC_OPTION_TABLENAME):
                for expiry in expiries:
                    finalTableName = HISTORIC_OPTION_TABLENAME + symbol + expiry
                    self.tableNameToTypeSet.update({finalTableName : "kHistoricOption"})

            elif (tableName == utility.HISTORIC_STOCK_TABLENAME):
                if type(symbol)==list:
                    for s in symbol:
                        finalTableName = HISTORIC_STOCK_TABLENAME + s
                        self.tableNameToTypeSet.update({finalTableName : "kHistoricStock"})
                else:
                  finalTableName = HISTORIC_STOCK_TABLENAME + symbol
                  self.tableNameToTypeSet.update({finalTableName : "kHistoricStock"})


    def CreateTables(self):
        for iter in self.tableNameToTypeSet.iteritems():
            
            dropSQL = "DROP TABLE %s" %(iter[0])

            SQL = ""
            if (iter[1] == "kLiveOption"):
                SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, Symbol VARCHAR(20), TimeStamp INT NOT NULL,OptionType VARCHAR(3), 
                    Expiry VARCHAR(7) NOT NULL, StrikePrice INT NOT NULL, NoOfContracts INT NOT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL, LTP FLOAT NOT NULL, NetChange FLOAT NOT NULL,
                    ImpliedVolatility FLOAT NOT NULL, PRIMARY KEY (id)); """ % ( iter[0])

            elif (iter[1] == "kHistoricOption"):
                SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, Date INT NOT NULL,OptionType VARCHAR(3), 
                    StrikePrice INT NOT NULL, Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    NoOfContracts INT NOT NULL,Turnover FLOAT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL, PRIMARY KEY (id)); """ % ( iter[0])

            elif (iter[1] == "kHistoricStock"):
                SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, Date INT NOT NULL, Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    SharesTraded INT NOT NULL,Turnover FLOAT NULL, PRIMARY KEY (id)); """ % ( iter[0])

            try:
                # Lets not drop table
                #self.cursor.execute(dropSQL)
                a = True        # PlaceHolder comment
            except Exception as e:
                print e

            try:
                self.cursor.execute(SQL)
            except Exception as e:
                print e
                print "mainDBCreator.py file"


if __name__ == "__main__":
    db = kInitialize();
    db()