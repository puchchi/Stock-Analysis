import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.dirname( path.abspath(__file__) ) ) ) )
#sys.path.append( path.dirname( path.abspath(__file__) ) )

import MySQLdb, datetime
import csv
from scraper.utility import *
from MainDriver import ComputeIndicators
from multiprocessing import Process, Queue

class kCreateSpotCSVDataFile():

    def __init__(self, symbol, startDate, endDate):
        self.symbol = symbol
        self.historicTableName = HISTORIC_STOCK_TABLENAME + symbol
        self.liveTableName = LIVE_STOCK_TABLENAME
        self.startDate = int(datetime.datetime.strptime(startDate, "%d-%b-%Y").strftime("%Y%m%d"))
        self.endDate = int(datetime.datetime.strptime(endDate, "%d-%b-%Y").strftime("%Y%m%d"))
        self.fileName = CSV_DATA_DIRECTORY + symbol + CSV_EXTENSION
        try:
            self.db = MySQLdb.connect(DATABASE_HOST, DATABASE_USERNAME,
						    DATABASE_PASSWORD, DATABASE_NAME, charset="utf8", use_unicode=True)
        except Exception as e:
            print "Error in connecting Mysql db in CreateCSVDataFile.py"

    def __call__(self):
        SQL = """select Date, Open, High, Low, Close, SharesTraded from %s where Date >= %s and Date <= %s order by Date asc
                """ %(self.historicTableName, self.startDate, self.endDate)
        
        try:
            # Cursor will used in executing SQL query
            cursor = self.db.cursor()  
            cursor.execute(SQL)
            row = cursor.fetchall()

            # adding headers to csv file
            header = "Date,Open,High,Low,Close,Volume\n"
            with open(self.fileName, 'wb') as fp:
                fp.write(header)

            with open(self.fileName, 'ab') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(row)

            # Adding live row
            liveSQL = """select Open, High, Low, LTP, Volume from %s where symbol='%s' and timestamp=(select max(timestamp) from %s where symbol='%s')""" %(self.liveTableName, self.symbol, self.liveTableName, self.symbol)
            cursor.execute(liveSQL)
            liveRow = cursor.fetchall()
            if (liveRow.__len__()>0):
                liveRow = list(liveRow[0])
                liveRow.insert(0, self.endDate)
                tempRow = (liveRow,)

                with open(self.fileName, 'ab') as fp:
                    a = csv.writer(fp, delimiter=',')
                    a.writerows(tempRow)

            cursor.close()
        except Exception as e:
            print e
            print "Error in CreateSpotCSVDataFile.py"
            

class kCommand:

    def __init__(self, *args):
        self.args = args

    def run_job(self, queue, args):
        try:
            createCSVDataFile = kCreateSpotCSVDataFile(symbol=self.args[0][0], startDate=self.args[0][1], endDate=CURRENT_DATE)
            createCSVDataFile()
            queue.put(None)
        except Exception as e:
            queue.put(e)

        try:
            # To compute all of the indicator, use __call__ api 
            computeIndicator = ComputeIndicators.kComputeIndicators(symbol=self.args[0][0])
            #computeIndicator()
            computeIndicator.calculateADX()
        except Exception as e:
            print e

    def do(self):

        queue = Queue()
        process = Process(target=self.run_job, args=(queue, self.args))
        process.start()
        result = queue.get()
        process.join()

        if result is not None:
            raise result

    def get_name(self):
        return "Creating CSV file Command"

if __name__ == "__main__":
    startDate = datetime.datetime.strptime("01-Jan-2018", "%d-%b-%Y").strftime("%d-%b-%Y")
    createCSVDataFile = kCreateSpotCSVDataFile("SBIN", startDate, CURRENT_DATE)
    createCSVDataFile()
