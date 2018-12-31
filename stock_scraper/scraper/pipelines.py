'''This module is used to connect to MySQL database having
    database name StockDB,with user StockUser. This module
    will check & parse & insert data in database
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
from scraper import utility
from scrapy.exceptions import DropItem
import logging
import datetime

# start logger
log = logging.getLogger(__name__)

class kStockScraperPipeline(object):
    
    def __init__(self):    
        self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
        # Cursor will used in executing SQL query
        self.cursor = self.db.cursor()

    
    def process_item(self, item, spider):
        # StockOptionSpider pipeline #_OBSOLETE_
        #if spider.name == 'kStockOptionSpider':
        #    return AddStockOptionToDB(item)
            
        # kOptionValueSpider pipeline
        if spider.name == 'kHistoricOptionSpider':
            return self.AddOptionToDB(item)
              
        # kLiveOptionValueSpider pipeline
        if spider.name == 'kLiveOptionSpider':
            return self.AddLiveOptionToDB(item)

        if spider.name == 'kLiveEquitySpider' or spider.name == 'kLiveIndexSpider':
            return self.AddLiveStockToDB(item)
              
        if spider.name == 'kLiveFutureSpider':
            return self.AddLiveFutureToDB(item)

        if spider.name == 'kHistoricIndexSpider' or spider.name == 'kHistoricEquitySpider':
            return self.AddStockToDB(item)

        return item


    def AddStockToDB(self, item):
        tableName = item['DatabaseTableName']
        SQL = """ INSERT INTO %s( Date,Open,High,Low,Close,SharesTraded,Turnover)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        """ % (tableName, item['Date'].encode('utf-8'), item['Open'].encode('utf-8'), item['High'].encode('utf-8'),
                item['Low'].encode('utf-8'), item['Close'].encode('utf-8'), item['SharesTraded'].encode('utf-8'),
                item['Turnover'].encode('utf-8'))
   
        primaryKey = ['Date']
        primartKeyVal = [item['Date']]

        try:
            if (self.CheckPrimaryKey(primaryKey, primartKeyVal, tableName) == False):
                self.cursor.execute(SQL)
                self.db.commit()
        except:
            self.db.rollback()
        return item

    
    def AddOptionToDB(self, item):
        expiry = item['Expiry']
        expiry = expiry.split('-')
        #tableName = utility.dbTableNameOption + expiry[1] + expiry[2]
        tableName = item["DatabaseTableName"] + expiry[1] + expiry[2]

        primaryKey = ['Date', 'OptionType', 'StrikePrice']
        primartKeyVal = [item['Date'], item['OptionType'], item['StrikePrice']]
        

        SQL = """
            INSERT INTO %s (Date , OptionType, StrikePrice , Open , High , Low , Close , NoOfContracts , Turnover , OpenInterest , ChangeInOI)
            VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """ % (tableName, item['Date'].encode('utf-8'), item['OptionType'].encode('utf-8'), item['StrikePrice'].encode('utf-8'), item['Open'].encode('utf-8'), item['High'].encode('utf-8'),
                item['Low'].encode('utf-8'), item['Close'].encode('utf-8'), item['NoOfContracts'].encode('utf-8'), item['Turnover'].encode('utf-8'), 
                item['OpenInterest'].encode('utf-8'), item['ChangeInOI'])

        try:
            if (self.CheckPrimaryKey(primaryKey, primartKeyVal, tableName) == False):
                self.cursor.execute(SQL)
                self.db.commit()
        except:
            self.db.rollback()
        return item 


    def AddLiveOptionToDB(self, item):
        #tableName = utility.dbTableNameLiveOption 
        tableName = item["DatabaseTableName"]
        #timestamp = int(datetime.datetime.strftime(datetime.datetime.now(), "%H%M"))
        timestamp = int(item["TimeStamp"])
        symbol = item["Symbol"]
        expiry = item["Expiry"]

        # Since we are getting LTPCall & LTPPut as list
        SQLCall = """
            INSERT INTO %s (Symbol, TimeStamp , OptionType, Expiry, StrikePrice, NoOfContracts , OpenInterest , ChangeInOI, LTP, NetChange, ImpliedVolatility)
            VALUES ('%s', %s,'%s','%s',%s,%s,%s,%s,%s,%s, %s)
        """ % (tableName, symbol, timestamp, "CE", expiry, item['StrikePrice'].encode('utf-8'), item['VolumeCall'].encode('utf-8'), item['OpenInterestCall'].encode('utf-8'), 
                item['ChangeInOICall'].encode('utf-8'), item['LTPCall'][0].encode('utf-8'), item['NetChangeCall'].encode('utf-8'),
                item['ImpliedVolatilityCall'].encode('utf-8')) 

        primaryKeyCall = ['Symbol', 'TimeStamp', 'OptionType', 'StrikePrice', 'Expiry']
        primaryKeyCallVal = [symbol, timestamp, 'CE', item['StrikePrice'].encode('utf-8'), expiry]
        #print SQLCall

        SQLPut = """
            INSERT INTO %s (Symbol, TimeStamp , OptionType, Expiry, StrikePrice, NoOfContracts , OpenInterest , ChangeInOI, LTP, NetChange, ImpliedVolatility)
            VALUES ('%s', %s,'%s','%s', %s,%s,%s,%s,%s,%s, %s)
        """ % (tableName, symbol, timestamp, "PE", expiry, item['StrikePrice'].encode('utf-8'), item['VolumePut'].encode('utf-8'), item['OpenInterestPut'].encode('utf-8'), 
                item['ChangeInOIPut'].encode('utf-8'), item['LTPPut'][0].encode('utf-8'), item['NetChangePut'].encode('utf-8'),
                item['ImpliedVolatilityPut'].encode('utf-8')) 

        primaryKeyPut = ['Symbol', 'TimeStamp', 'OptionType', 'StrikePrice', 'Expiry']
        primaryKeyPutVal = [symbol, timestamp, 'PE', item['StrikePrice'], expiry]

        try:
            if (self.CheckPrimaryKey(primaryKeyCall, primaryKeyCallVal, tableName) == False):
                self.cursor.execute(SQLCall)
                self.db.commit()
            
            if (self.CheckPrimaryKey(primaryKeyPut, primaryKeyPutVal, tableName) == False):
                self.cursor.execute(SQLPut)
                self.db.commit()
        except:
            self.db.rollback()
        return item 

    
    def AddLiveStockToDB(self, item):
        tableName = item["DatabaseTableName"]
        #timestamp = int(datetime.datetime.strftime(datetime.datetime.now(), "%H%M"))
        timestamp = int(item["TimeStamp"])

        primaryKey = ['Symbol', 'TimeStamp']
        primartKeyVal = [item['Symbol'], timestamp]

        SQL = """
            INSERT INTO %s (Symbol, timestamp, Open , High , Low , LTP , NetChange , PerChange , Volume , Turnover)
            VALUES ('%s',%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """ % (tableName, item['Symbol'].encode('utf-8'), timestamp, item['Open'].encode('utf-8'), item['High'].encode('utf-8'),
                item['Low'].encode('utf-8'), item['LTP'].encode('utf-8'), item['TotalChange'].encode('utf-8'), item['PerChange'].encode('utf-8'), 
                item['Volume'].encode('utf-8'), item['Turnover'].encode('utf-8'))

        try:
            if (self.CheckPrimaryKey(primaryKey, primartKeyVal, tableName) == False):
                self.cursor.execute(SQL)
                self.db.commit()
        except:
            self.db.rollback()
        return item 


    def AddLiveFutureToDB(self, item):
        print "Implement me"


    def CheckPrimaryKey(self, rowList, rowValues, tableName):
        SQL = """SELECT * FROM %s where """ %(tableName)

        for i in range(rowList.__len__()):
            if (i != 0):
                SQL = SQL + " and "
            val = ""
            val = "\"" + str(rowValues[i]) + "\""
            #if type(rowValues[i]) == str:
            #    val = "\"" + rowValues[i] + "\""
            #else:
            #    val = str(rowValues[i])
            SQL = SQL + " " + rowList[i] + "=" + val

        try:
            self.cursor.execute(SQL)
            if self.cursor.rowcount == 0:
                return False
        except Exception as e:
            print e
            print "Exception in checkPrimaryKey in pipeline.py"
            return False
        return True


    def close_spider(self, spider):
        self.db.close()
