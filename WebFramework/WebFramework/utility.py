# This module wii be in sync with stock_scraper project utility file

import MySQLdb, smtplib, datetime
from os import path

# data for whole framework

DATABASE_HOST = "localhost"
DATABASE_NAME = "StockDB"
DATABASE_USERNAME = "StockUser"
DATABASE_PASSWORD = "StockPass"

MAXVALUE = 999999999999

# defs
CURRENT_EXPIRY =                ["May2018", "Jun2018", "Jul2018"]
LIVE_OPTION_TABLENAME =         "LiveOption"
LIVE_STOCK_TABLENAME =          "LiveStock"                                         # For live equity & live index
HISTORIC_OPTION_TABLENAME =     "HistoricOption"
HISTORIC_STOCK_TABLENAME =      "HistoricStock"                                 # For historic index & equity
TIMEDELTA =                     3               # used for historic spider
HISTORIC_START_DATE =           "01-Jan-2018"
CURRENT_DATE =                  datetime.datetime.now().strftime("%d-%b-%Y")    # 01-Jan-2018
CSV_DATA_DIRECTORY =            path.dirname( path.dirname(path.abspath(__file__))) + "\\data\\"
CSV_EXTENSION =                 ".csv"
CSV_INDICATOR_EXTENSTION =      "Indicator.csv"
START_INDEX =                   30      # How many rows we need to scrape from csv file from start
END_INDEX =                     7

# Mail Info
RECIPIENT =                     ["anursin@adobe.com"]
SMTP_SERVER_NAME =              "mailsea.sea.adobe.com"
MAIL_SENDER =                   "anursin@adobe.com"


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


def GETDB():
    try:
        return MySQLdb.connect(DATABASE_HOST, DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_NAME, charset="utf8", use_unicode=True)
    except Exception as e:
        print e
        print "Error connecting database"
    