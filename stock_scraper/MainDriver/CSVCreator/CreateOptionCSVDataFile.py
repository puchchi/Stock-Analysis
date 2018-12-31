import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.abspath(__file__) ) )

import MySQLdb
import csv
from scraper import utility

class kCreateOptionCSVDataFile():

    def __init__(self, tableNames, filenames):
        self.tableNames = tableNames
        self.fileNames = filenames
        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
        except Exception as e:
            print "Error in connecting Mysql db in CreateCSVDataFile.py"

    def __call__(self):

        for i in range(len(self.tableNames)):
            SQL = """select Date, OptionType, StrikePrice, Open, High, Low, Close,
                     NoOfContracts, TurnOver, OpenInterest, ChangeInOI from %s order by Date asc
                    """ %(self.tableNames[i])
            # Cursor will used in executing SQL query
            cursor = self.db.cursor() 
            try: 
                cursor.execute(SQL)
            except Exception as e:
                print "Error in executing SQL query in CreatOptionCSVDataFile"
                print e
            row = cursor.fetchall()
        
            # adding headers to csv file
            header = "Date,OptionType,StrikePrice,Open,High,Low,Close,NoOfContracts,TurnOver,OpenInterest,ChangeInOI\n"
            with open(self.fileNames[i], 'wb') as fp:
                fp.write(header)

            with open(self.fileNames[i], 'ab') as fp:
                a = csv.writer(fp, delimiter=',')
                a.writerows(row)

        cursor.close()


if __name__ == "__main__":
    createCSVDataFile = kCreateOptionCSVDataFile([], [])
    createCSVDataFile()
