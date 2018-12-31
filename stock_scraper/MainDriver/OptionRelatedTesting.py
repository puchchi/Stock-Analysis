import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import MySQLdb
import pandas as pd
from scraper import utility

class kOptionRelatedTesting:
    def __init__(self, csvFileName):
        #parser = lambda date: pd.datetime.strptime(date, '%Y%m%d')
        self.df = pd.read_csv(csvFileName)#, parse_dates = [0], date_parser = parser, index_col = "Date")

        try:
            self.db = MySQLdb.connect(utility.databaseHost, utility.databaseUsername,
						    utility.databasePassword, utility.databaseName, charset="utf8", use_unicode=True)

        except Exception as e:
            print "Error in kOptionRelatedTesting connecting MYSQLdb.py"

    def __call__(self):
        #self.plotOIGraphs()
        self.plotOIGraph2()

    def plotOIGraph2(self):

        ceOISQL = """ select date ,sum(OpenInterest) from %s where optiontype="%s" group by date
                """ %(utility.dbTableNameByOptionExpiry, "CE")
        peOISQL = """ select date ,sum(OpenInterest) from %s where optiontype="%s" group by date
                """ %(utility.dbTableNameByOptionExpiry, "PE")
        cursor = self.db.cursor()  
        cursor.execute(ceOISQL)
        ceRows = cursor.fetchall()

        cursor.execute(peOISQL)
        peRows = cursor.fetchall()
        #print rows[0][0]
        oiSeries = [["Date", "CE OI", "PE OI", "Nifty"]]
        dates = []

        if len(ceRows) != len(peRows):
            print "Error CE and PE Rows out of sync"
            return

        for i in range(len(ceRows)):
            dates.append(ceRows[i][0])
            #oiSeries.append([utility.dateDecoding(ceRows[i][0]), int(ceRows[i][1]), int(peRows[i][1])])

        spotValueSQL = """select date, close from %s where date >= %s and date <= %s
                        """ %(utility.dbTableName, min(dates), max(dates))

        cursor.execute(spotValueSQL)
        spotValue = cursor.fetchall()
        #print spotValue
        for i in range(len(ceRows)):
            #dates.append(ceRows[i][0])
            oiSeries.append([utility.dateDecoding(ceRows[i][0]), int(ceRows[i][1]), int(peRows[i][1]), spotValue[i][1]])
        print oiSeries
        cursor.close()

    def plotOIGraphs(self):
        groups = self.df.groupby(["Date", "OptionType"]).groups
        ceOISeries = []
        peOISeries = []
        for i in groups.iteritems():
            oiSum = 0
            for j in i[1]:
                #print groups[i][j]
                oiSum += self.df.iloc[j]["OpenInterest"]
            if i[0][1] == "CE":
                #print str(i[0][0]) + " ce   " + str(oiSum)
                ceOISeries.append(oiSum)
            elif i[0][1] == "PE":
                #print str(i[0][0]) + "  pe  " + str(oiSum)
                peOISeries.append(oiSum)
        print ceOISeries
        print peOISeries