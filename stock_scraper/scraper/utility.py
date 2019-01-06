# This module contains common function 

import MySQLdb, smtplib, datetime
from os import path

# data for whole framework
databaseHost = "localhost"
databaseName = "StockDB"
databaseUsername = "StockUser"
databasePassword = "StockPass"

DATABASE_HOST = "localhost"
DATABASE_NAME = "StockDB"
DATABASE_USERNAME = "StockUser"
DATABASE_PASSWORD = "StockPass"

MAXVALUE = 999999999999

# defs
CURRENT_EXPIRY =                ["Jan2019", "Feb2019"]
LIVE_OPTION_TABLENAME =         "LiveOption"
LIVE_STOCK_TABLENAME =          "LiveStock"                                         # For live equity & live index
HISTORIC_OPTION_TABLENAME =     "HistoricOption"
HISTORIC_STOCK_TABLENAME =      "HistoricStock"                                 # For historic index & equity
TIMEDELTA =                     3               # used for historic spider
HISTORIC_START_DATE =           "01-Jan-2018"   # It will be used only once, then we will false coldstart and crawl only 3 days behind
CURRENT_DATE =                  datetime.datetime.now().strftime("%d-%b-%Y")    # 01-Jan-2018
INDICATOR_START_DATE =          (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%d-%b-%Y")
CSV_DATA_DIRECTORY =            path.dirname( path.dirname(path.abspath(__file__))) + "\\data\\"
CSV_SINGAL_DATA_DIRECTORY =     CSV_DATA_DIRECTORY + "signal\\"
CURRENCY_DIRECTORY =            CSV_DATA_DIRECTORY + "currency\\"
CSV_EXTENSION =                 ".csv"
CSV_INDICATOR_EXTENSTION =      "Indicator.csv"
SIGNAL_TEST_RESULT =            "SignalTestResult"
START_INDEX =                   30      # How many rows we need to scrape from csv file from start
END_INDEX =                     7
TARGET_PRICE_1 =                1   #1%
TARGET_PRICE_2 =                2 #2%
TARGET_PRICE_3 =                3   #3%
STOP_LOSS =                     2.5    #2.5%
NIFTY_STOCK_LIST =              ["SBIN", "ICICIBANK", "HDFC", "KOTAKBANK", "HDFCBANK", "AXISBANK", "TATASTEEL", "CIPLA", "INFY", "BPCL", "COALINDIA", 
             "NTPC", "POWERGRID", "ONGC", "BAJFINANCE", "INFRATEL", "JSWSTEEL", "TATAMOTORS", "HEROMOTOCO", "SUNPHARMA", "DRREDDY",
             "HCLTECH", "ULTRACEMCO", "HINDUNILVR", "VEDL", "GRASIM", "TECHM","INDUSINDBK", "GAIL","ASIANPAINT", "EICHERMOT",
             "RELIANCE", "BHARTIARTL", "TITAN", "WIPRO", "INFY", "MARUTI", "IBULHSGFIN", "ZEEL", "ADANIPORTS", "UPL", "IOC", "BAJAJFINSV"]

# Mail Info
RECIPIENT =                     ["anursin@adobe.com"]
SMTP_SERVER_NAME =              "mailsea.sea.adobe.com"
MAIL_SENDER =                   "anursin@adobe.com"


# Not needed for automatic crawling
stockName = "SBIN"      # Option symbol of nifty is "NIFTY", "SBIN", "ICICIBANK", "HDFC", "INFY", "TATASTEEL"
                            #  "CIPLA", "KOTAKBANK", "HDFCBANK", "AXISBANK", 
stockList = ["SBIN", "ICICIBANK", "HDFC", "KOTAKBANK", "HDFCBANK", "AXISBANK", "TATASTEEL", "CIPLA", "INFY", "BPCL", "COALINDIA", 
             "NTPC", "POWERGRID", "ONGC", "BAJFINANCE", "INFRATEL", "JSWSTEEL", "TATAMOTORS", "HEROMOTOCO", "SUNPHARMA", "DRREDDY",
             "HCLTECH", "ULTRACEMCO", "HINDUNILVR", "VEDL", "GRASIM", "TECHM","INDUSINDBK", "GAIL","ASIANPAINT", "EICHERMOT",
             "RELIANCE", "BHARTIARTL", "TITAN", "WIPRO", "INFY", "MARUTI", "IBULHSGFIN", "ZEEL", "ADANIPORTS", "UPL", "IOC", "BAJAJFINSV"]
stockType = "Equity"     # Index or Equity or LiveOption
dbTableName = HISTORIC_STOCK_TABLENAME + stockName
dbTableNameOption = HISTORIC_OPTION_TABLENAME + stockName    # Final table name will be OptionValueOfNiftyJan2018
dbTableNameLiveOption = LIVE_STOCK_TABLENAME + stockName     
csvFileName = "data/Nifty.csv"
csvFileNameOption = "data/NiftyOption"            #append .CSV in function
csvFileNameWithIndicators = "data/NIFTYIndicator.csv"
startYear = 2010
endYear = 2019              # expected year + 1
testDataDateLower ="01-Jan-2019" # Date from which backward test signal will get genrated
testDataDateUpper ="31-Dec-2019"
endMonth = "Mar"
dbStartDate = 20180101      #yyyymmdd
dbEndDate = 20181231
startIndex = 30             # How many rows we need to scrape from csv file from start
endIndex = 7                
timeIntervalBetweenScrape = 60      #in seconds
thresholdPassFailPer = 75

# To get symbol count from NSE, use following url
# https://www.nseindia.com//marketinfo/sym_map/symbolCount.jsp?symbol=HDFC
# by default symbolcount is 1, if its other than 1, define here
SYMBOL_COUNT = {"HDFC":2, 
    }


# Option Data
expiries = ["Jan2019", "Feb2019", "Mar2019"]       #Standard "Jan2018"
daysBetweenExpiry = 100                 #Its 90 but we are taking 100 for any boundry cases
instrumentType = "OPTIDX"               # OPTIDX FUTIDX OPTSTK FUTSTK
optionCSVFileForTesting = "data/NiftyOptionMar2018.csv"
dbTableNameByOptionExpiry = "OptionValueOfNiftyMar2018"


# this will define lower n upper range of option
optionRange = 2500
strikePriceGap = 50
monthToNumberHash = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07',
                    'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12', 'jan':'01', 'feb':'02',
                    'mar':'03', 'apr':'04', 'may':'05', 'jun':'06', 'jul':'07', 'aug':'08', 'sep':'09',
                    'oct':'10', 'nov':'11', 'dec':'12'
                    }


# following list contains expiry date of all years since 2005
indexExpiryDate = {2000:["29-06-2000", "27-07-2000", "31-08-2000", "28-09-2000", "25-10-2000", "30-11-2000", "28-12-2000"],
                 2001:["25-01-2001", "22-02-2001", "29-03-2001", "26-04-2001", "31-05-2001", "28-06-2001", "26-07-2001", "30-08-2001", "27-09-2001", "25-10-2001", "29-11-2001", "27-12-2001"],
                 2002:["31-01-2002", "28-02-2002", "28-03-2002", "25-04-2002", "30-05-2002", "27-06-2002", "25-07-2002", "29-08-2002", "26-09-2002", "31-10-2002", "28-11-2002", "26-12-2002"],
                 2003:["30-01-2003", "27-02-2003", "27-03-2003", "24-04-2003", "29-05-2003", "26-06-2003", "31-07-2003", "28-08-2003", "25-09-2003", "30-10-2003", "27-11-2003", "27-02-2003"],
                 2004:["29-01-2004", "26-02-2004", "25-03-2004", "29-04-2004", "27-05-2004", "24-06-2004", "29-07-2004", "26-08-2004", "30-09-2004", "28-10-2004", "25-11-2004", "30-12-2004"],
                 2005:["27-01-2005", "24-02-2005", "31-03-2005", "28-04-2005", "26-05-2005", "30-06-2005", "28-07-2005", "25-08-2005", "29-09-2005", "27-10-2005", "24-11-2005", "29-12-2005"],
                 2006:["25-01-2006", "23-02-2006", "30-03-2006", "27-04-2006", "25-05-2006", "29-06-2006", "27-07-2006", "31-08-2006", "28-09-2006", "26-10-2006", "30-11-2006", "28-12-2006"],
                 2007:["25-01-2007", "22-02-2007", "29-03-2007", "26-04-2007", "31-05-2007", "28-06-2007", "26-07-2007", "30-08-2007", "27-09-2007", "25-10-2007", "29-11-2007", "27-12-2007"],
                 2008:["31-01-2008", "28-02-2008", "27-03-2008", "24-04-2008", "29-05-2008", "26-06-2008", "31-07-2008", "28-08-2008", "25-09-2008", "29-10-2008", "27-11-2008", "25-12-2008"],
                 2009:["29-01-2009", "26-02-2009", "26-03-2009", "30-04-2009", "28-05-2009", "25-06-2009", "30-07-2009", "27-08-2009", "24-09-2009", "29-10-2009", "26-11-2009", "31-12-2009"],
                 2010:["28-01-2010", "25-02-2010", "25-03-2010", "29-04-2010", "27-05-2010", "24-06-2010", "29-07-2010", "26-08-2010", "30-09-2010", "28-10-2010", "25-11-2010", "30-12-2010"],
                 2011:["27-01-2011", "24-02-2011", "31-03-2011", "28-04-2011", "26-05-2011", "30-06-2011", "28-07-2011", "25-08-2011", "29-09-2011", "25-10-2011", "24-11-2011", "29-12-2011"],
                 2012:["25-01-2012", "23-02-2012", "29-03-2012", "26-04-2012", "31-05-2012", "28-06-2012", "26-07-2012", "30-08-2012", "27-09-2012", "25-10-2012", "29-11-2012", "27-12-2012"],
                 2013:["31-01-2013", "28-02-2013", "28-03-2013", "25-04-2013", "30-05-2013", "27-06-2013", "25-07-2013", "29-08-2013", "26-09-2013", "31-10-2013", "28-11-2013", "26-12-2013"],
                 2014:["30-01-2014", "26-02-2014", "27-03-2014", "24-04-2014", "29-05-2014", "26-06-2014", "31-07-2014", "28-08-2014", "25-09-2014", "30-10-2014", "27-11-2014", "24-12-2014"],
                 2015:["29-01-2015", "26-02-2015", "26-03-2015", "30-04-2015", "28-05-2015", "25-06-2015", "30-07-2015", "27-08-2015", "24-09-2015", "29-10-2015", "26-11-2015", "31-12-2015"],
                 2016:["28-01-2016", "25-02-2016", "31-03-2016", "28-04-2016", "26-05-2016", "30-06-2016", "28-07-2016", "25-08-2016", "29-09-2015", "27-10-2015", "24-11-2016", "29-12-2016"],
                 2017:["26-01-2017", "23-02-2017", "30-03-2017", "27-04-2017", "25-05-2017", "29-06-2017", "27-07-2017", "31-08-2017", "28-09-2017", "26-10-2017", "30-11-2017", "28-12-2017"],
                 2018:["25-01-2018", "22-02-2018", "28-03-2018", "26-04-2018", "31-05-2018", "28-06-2018", "26-07-2018", "30-08-2018", "27-09-2018", "25-10-2018", "29-11-2018", "27-12-2018"],
                 2019:["31-01-2019", "28-02-2019", "28-03-2019", "25-04-2019", "30-05-2019", "27-06-2019", "25-07-2019", "29-08-2019", "26-09-2019", "31-10-2019", "28-11-2019", "26-12-2019"],
                 }

# This will convert 12-Jan-2014 to 20140112(yyyymmdd)
def dateEncoding(date):  # This function will convert date(string) to date(integer) format
    words = date.split('-')  # Spliting date using '-' as delimiter
    #return unicode(int(words[0] + monthToNumberHash[words[1]] + words[2])) 
    return unicode(int(words[2] + monthToNumberHash[words[1]] + words[0])) 

# From 20140130 to 30-Jan-2014
def dateDecoding(date):
    date = datetime.datetime.strptime(str(date), "%Y%m%d")
    return date.strftime("%d-%b-%Y")

# This will convert '7,500.00' to '7500.00'
def strToFloatNumber(data):
    if data.find('-')>-1:
        return unicode(float(0))

    # If data contains ',' e.g '7,500.00'
    if data.find(',') > 0:
        # Remove ',' e.g '7,500.00' will become '7500.00'
        data = data.replace(',', '')
    # Convert str to float
    return unicode(float(data))

# This will convert '7,500.00' to '7500'
def strToIntNumber(data):
    if data.find('-')>-1:
        return unicode(int(0))
    # If data contains ',' e.g '7,500.00'
    if data.find(',') > 0:
        # Remove ',' e.g '7,500.00' will become '7500.00'
        data = data.replace(',', '')
    return unicode(int(float(data.encode('utf-8'))))
    
# This will encode 12-Jan-2014 to 12012014 & CE to CE & 7,500.00 to 7500
# and then it will join by Join() processor
def expiryEncoding(data):
    # If data is formal date e.g 12-Jan-2014
    if data.find('-') > 0:    
        return dateEncoding(data)
    # If data is option type e.g CE or PE
    elif data == 'CE' or data == 'ce' or data == 'PE' or data == 'pe':
        return data
    # If data is strike price e.g '7,500.00'
    else:
        return strToIntNumber(data)
        


def getSpotValue(date):
    mysql = MySQLdb.connect('localhost', 'StockUser', 'StockPass', 'StockDB', charset="utf8", use_unicode=True)
    cursor = mysql.cursor()
    SQL = """
        select Close from %s where Date= %s;
    """ % (dbTableName, str(date).encode('utf-8'))
    print SQL
    cursor.execute(SQL)
    #This will check no of rows in output of query
    rowCount=cursor.rowcount
    if rowCount==0:
        spotValue=-1
    else:
        # fetchone mudule will fetch first row of result
        spotValue = int(cursor.fetchone()[0])
    #closing db connection
    mysql.close()
    return spotValue

def IsWeekday(datetime):
    if datetime.day!=6 and datetime != 7:
        return True
    return False

# Equities spot value url
# https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=sbin&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=01-01-2018&toDate=05-01-2018&dataType=PRICEVOLUMEDELIVERABLE

# NIFTY 50 ->SpotValueOfNifty
# Nifty Bank->SpotValueOfNiftyBank

def SENDMAIL(subject, content):
	try:
		server = smtplib.SMTP(SMTP_SERVER_NAME)
		for r in RECIPIENT:
			try:  # smtplib may raise except
				#date = time.ctime(time.time())
				date = datetime.datetime.now().strftime("%d-%m-%Y : %H:%M")
				header = ('From: %s\nTo: %s\nSubject: %s\n'
						% (MAIL_SENDER, r, subject))
				failed = True  # or return failed Tos dict
				failed = server.sendmail(MAIL_SENDER, r, header + content)
			except Exception as e:
				print "Failed in sendMail"
				print e
			finally:
				if failed:
					print 'Send mail error\nFailed recipients:\n' + str(failed)
				else:
					print 'Mail sent at : ' + date 
					print "Content: " + content

		server.quit()
	except Exception as e:
		print "Failed in sendMail"
		print e