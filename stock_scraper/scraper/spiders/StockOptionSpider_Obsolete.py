# Obsolete
# Use it for year wise data only
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scrapy, scraper.spiders, logging
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scraper import utility
from scraper.items import StockOptionItem
from scrapy.loader.processors import Join, MapCompose

# start logger
log = logging.getLogger(__name__)

class kStockOptionSpider(scrapy.Spider):
    
    name = 'kStockOptionSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, startYear, endYear, * args, **kwargs):
        super(kStockOptionSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.startYear = startYear
        self.endYear = endYear
        
    def start_requests(self):
        scrapy.Spider.start_requests(self)
        log.info("Creating start URL list: ")
        
        yearIter = self.startYear
        while yearIter <= self.endYear:
            
            for monthIter in range(0,12):
                # expiryDate is expiry date of any option
                expiryDate = utility.indexExpiryDate[yearIter][monthIter]
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
                #expiryDate = utility.dateEncoding(expiryDate)
                # this will get Spot value of NIFTY for that day
                while True:                
                    spotValue = utility.getSpotValue(expiryDate)
                    #If on expiry day,market will close, then return value will be -1
                    if spotValue!=-1:
                        break
                    #Now we will decrease expiryDate by 1
                    expiryDate-=1000000                     
                #converting spotValue into multiple of 100, e.g. 7432 to 7400
                spotValue=int(spotValue/100)
                spotValue*=100            
                spotValuelwr = spotValue - utility.optionRange
                spotValueupr = spotValue + utility.optionRange                
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
                        log.info('Generating_URL_Stat: SP: %s , ED: %s ,OT: %s ,SD: %s ,ED: %s' % (strikePrice, toDate, optionType, fromDate, toDate))
                        flag += 1
                        request=scrapy.Request(url, self.parse)
                        request.meta['year']=yearIter
                        yield request
                    # Increasing lower range by strikePriceGap
                    spotValuelwr += utility.strikePriceGap                
            # increasing year by 1 unit
            yearIter += 1
    
    item_fields = {
                 'Date':'./td[2]/nobr/text()',
                 'Expiry':('./td[3]/nobr/text()','./td[4]//text()','./td[5]//text()'),
                 'Open':'./td[6]//text()',
                 'High':'./td[7]//text()',
                 'Low':'./td[8]//text()',
                 'Close':'./td[9]//text()',
                 'NoOfContracts':'./td[12]//text()',
                 'Turnover':'./td[13]//text()',
                 'OpenInterest':'./td[15]//text()',
                 'ChangeInOI':'./td[16]//text()'
                 }
    
    def parse(self, response):
        
        # Check for "No Records"
        if (response.xpath('//tr[3]/td/text()').extract()[0].find('No Records') > 0):
            log.info("No_Response_Recieved : %s" % (response.url))
        else:
            # Storing all selector except top 2(which contains waste data)
            res = response.xpath('//tr[position()>2]')
            for val in res:
                loader = ItemLoader(StockOptionItem(), val)
                loader.default_input_processor = MapCompose(unicode.strip)
                loader.default_output_processor = Join()
                # To iterate in item_fields dicts
                for item, xpath in self.item_fields.iteritems():
                    #We have to write all 'Expiry' query at once to avoid override of value
                    if item=='Expiry':
                        loader.add_xpath(item,xpath[0])
                        loader.add_xpath(item,xpath[1])
                        loader.add_xpath(item,xpath[2])
                    else:
                        loader.add_xpath(item, xpath)
                yield loader.load_item()                    
