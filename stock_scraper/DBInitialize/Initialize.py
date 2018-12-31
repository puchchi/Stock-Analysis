import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
from scraper import utility


class kInitialize():

	def __init__(self, tableName):
		self.tableName = tableName
		try:
			self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)
			# Cursor will used in executing SQL query
			self.cursor = self.db.cursor()
		except Exception as e:
			print "Error in connecting Mysql db in initialize.py"

	def __call__(self):
		SQL = ""
		dropTableCmd = ""
		if utility.stockType == "Index" or utility.stockType == "Equity":
			dropTableCmd = """ DROP TABLE %s;"""%(self.tableName)
			SQL = """ CREATE TABLE %s ( Date INT NOT NULL,Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    SharesTraded INT NOT NULL,Turnover FLOAT NULL,
				    PRIMARY KEY (Date)); """ % ( self.tableName)
		elif utility.stockType == "Option":
			dropTableCmd = """ DROP TABLE %s;""" %(self.tableName)
			SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, Date INT NOT NULL,OptionType VARCHAR(3), 
                    StrikePrice INT NOT NULL, Open FLOAT NOT NULL
				    ,High FLOAT NOT NULL,Low FLOAT NOT NULL,Close FLOAT NOT NULL,
				    NoOfContracts INT NOT NULL,Turnover FLOAT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL, PRIMARY KEY (id)); """ % ( self.tableName)
		elif utility.stockType == "LiveOption":
			dropTableCmd = """ DROP TABLE %s;""" %(self.tableName)

			SQL = """ CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT, TimeStamp INT NOT NULL,OptionType VARCHAR(3), 
                    StrikePrice INT NOT NULL, NoOfContracts INT NOT NULL, OpenInterest INT NOT NULL,
                    ChangeInOI INT NOT NULL, LTP FLOAT NOT NULL, NetChange FLOAT NOT NULL,
                    ImpliedVolatility FLOAT NOT NULL, PRIMARY KEY (id)); """ % ( self.tableName)
		try:
			#print SQL
            #dropping table
			self.cursor.execute(dropTableCmd)
			
		except Exception as e:
			print "Error in dropping table Call function."

		try:
			self.cursor.execute(SQL)
		except Exception as e:
			print "Error in creating table Call function."


if __name__ == "__main__":
    tableName = "SpotValueOfNiftyBank"
    db = kInitialize(tableName);
    db()