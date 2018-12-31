import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
sys.path.append( path.dirname( path.dirname( path.dirname(path.abspath(__file__)) ) ) )

import MySQLdb
from scraper import utility

class kCommand:

    def __init__(self, *args):
        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
				            utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
            # Cursor will used in executing SQL query
            self.cursor = self.db.cursor()
        except Exception as e:
            print e
            print "Error in connecting Mysql db in CleanNCreateLiveOptionDB.py"


    def do(self):
        tableName = utility.LIVE_OPTION_TABLENAME

        try:
            dropTableSQL = """ DROP TABLE %s;""" %(tableName)
            self.cursor.execute(dropTableSQL)
        except Exception as e:
            print "Error in dropping table Call function in CleanNCreateLiveOptionDB.py."

        try:
            SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, Symbol VARCHAR(20), TimeStamp INT NOT NULL,OptionType VARCHAR(3), 
                    Expiry VARCHAR(7) NOT NULL, StrikePrice INT NOT NULL, NoOfContracts INT NOT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL, LTP FLOAT NOT NULL, NetChange FLOAT NOT NULL,
                    ImpliedVolatility FLOAT NOT NULL, PRIMARY KEY (id)); """ % (tableName)
            self.cursor.execute(SQL)
        except Exception as e:
            print "Error in creating table Call function in CleanNCreateLiveOptionDB.py."

    def get_name(self):
        return "Cleaning & creating live option DB Command"