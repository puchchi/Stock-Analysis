import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from scraper import utility
import logging
#import stock_scraper

#logging.basicConfig(filename='/root/stock_scraper/stock_scraper.log',filemode='a',format='%(asctime)-15s : %(module)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
log = logging.getLogger(__name__)


def start_requests():
    #scrapy.Spider.start_requests(self)
    #log.info("Creating start URL list: ")
    startYear=2014
    endYear=2015
        
    yearIter = startYear
    while yearIter <= endYear:
            
        monthIter = 0
        
        #while monthIter<12:
        for monthIter in range(0,12):
    # expiryDate is expiry date of any option
            expiryDate = utility.indexExpiryDate[yearIter][monthIter]
            print expiryDate
              
              # Calculation of fromDate( date from which option life start)
               # if current month is jan,feb or mar
            if monthIter < 3:
                    # Go to previous year
                fromDate = utility.indexExpiryDate[(yearIter - 1)][(11 - 2 + monthIter)]
                # if current month is other than jan,feb & mar
            else:
                fromDate = utility.indexExpiryDate[yearIter][(monthIter - 3)]
                    
                # toDate is last date(aka expiry date) of an option
            toDate = expiryDate
                
                # this will convert "12-02-2014" to 12022014 to get spot value of NIFTY from database
            expiryDate = int(expiryDate.replace('-', ''))
                # this will get Spot value of NIFTY for that day
                
            while True:
                
                spotValue = utility.getSpotValue(expiryDate)
                #If on expiry day,market will close, then return value will be -1
                if spotValue!=-1:
                    break
                #Now we will decrease expiryDate by 1
                expiryDate-=1000000 
                
            print 'PRINTING_SPOT_VALUE : %s'%spotValue
            
            log.info('PRINTING_SPOT_VALUE : %s'%spotValue)
            
            temp=int(spotValue/100)
            temp*=100
            spotValuelwr = temp - utility.optionRange
            spotValueupr = temp + utility.optionRange
                
                
            log.info( '####################################################################################################################################')
            while spotValuelwr <= spotValueupr:
                flag = 1
                # strike price of option
                strikePrice = spotValuelwr
                    # symbol code of nifty is -10003
                    # To add url for CE & PE both
                while flag < 3:
                    if flag == 1:
                        optionType = 'CE'
                    else:
                        optionType = 'PE'
                    url = 'http://www.nseindia.com/products/dynaContent/derivatives/equities/histcontract.jsp?symbolCode=-10003&symbol=NIFTY&instrumentType=OPTIDX&symbol=NIFTY&expiryDate=%s&optionType=%s&strikePrice=%s&dateRange=&fromDate=%s&toDate=%s' % (toDate, optionType, strikePrice, fromDate, toDate)
                       # log.info('Generating_URL_Stat: %s'%url)
                    log.info( 'Generating_URL_Stat: SP: %s , ED: %s ,OT: %s ,SD: %s ,ED: %s' % (strikePrice, toDate, optionType, fromDate, toDate))
                    flag += 1
                    #request=scrapy.Request(url, self.parse)
                    #request.meta['year']=yearIter
                    #yield request
                    # Increasing lower range by strikePriceGap
                spotValuelwr += utility.strikePriceGap
                
            #    monthIter+=1
                
                
            # increasing year by 1 unit
            log.info( '####################################################################################################################################')
        yearIter += 1
        
if __name__=='__main__':
    start_requests()