import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import datetime
import scrapy, scraper.spiders, logging
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scraper import utility
from scraper.items import kHistoricOptionItem
from scrapy.loader.processors import Join, MapCompose

# start logger
log = logging.getLogger(__name__)

class kHistoricOptionSpider(scrapy.Spider):
    
    name = 'kHistoricOptionSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, instrumentType, databaseTableName, coldStart, expiries=[], * args, **kwargs):
        super(kHistoricOptionSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expiries = expiries
        self.instrumentType = instrumentType
        self.databaseTableName = databaseTableName + symbol
        self.coldStart = coldStart
        
    def start_requests(self):
        scrapy.Spider.start_requests(self)

        for expiry in self.expiries:
            temp = datetime.datetime.strptime(expiry, "%b%Y")   # Expiry are in "Jan2018" format.
            month = temp.month
            year = temp.year
            expiryDate = utility.indexExpiryDate[year][month-1]
            expiryDateStd = datetime.datetime.strptime(expiryDate, "%d-%m-%Y")
            dateList = [expiryDateStd - datetime.timedelta(days=x) for x in range(0, utility.daysBetweenExpiry)]
            
            if (self.coldStart == False):
                now = datetime.datetime.now()
                dateList = [now - datetime.timedelta(days=x) for x in range(0, utility.TIMEDELTA)]

            #Working URL
            # https://nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?instrumentType=OPTIDX&symbol=NIFTY&expiryDate=25-01-2018&optionType=CE&strikePrice=&dateRange=week&fromDate=03-Jan-2018&toDate=05-Jan-2018&segmentLink=9&symbolCount=
            # Referer: https://www.nseindia.com/products/content/derivatives/equities/historical_fo.htm

            for date in dateList:
                standardDate = date.strftime("%d-%b-%Y")
                for optionType in ["CE", "PE"]:
                    url = "https://nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?instrumentType=%s&symbol=%s&expiryDate=%s&optionType=%s&strikePrice=&dateRange=week&fromDate=%s&toDate=%s&segmentLink=9&symbolCount=" %(self.instrumentType, self.symbol, expiryDate, optionType, standardDate, standardDate)
                    request=scrapy.Request(url, self.parse, headers={'Referer':'https://www.nseindia.com/products/content/derivatives/equities/historical_fo.htm'})
                    yield request

    
    item_fields = {
                 'Date':'./td[2]/nobr/text()',
                 'Expiry':'./td[3]/nobr/text()',
                 'OptionType':'./td[4]//text()',
                 'StrikePrice':'./td[5]//text()',
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
        try:
            if (response.xpath('//tr[3]/td/text()').extract()[0].find('No Records') > 0):
                log.info("No_Response_Recieved : %s" % (response.url))
            else:
                # Storing all selector except top 2(which contains waste data)
                res = response.xpath('//tr[position()>2]')
                for val in res:
                    loader = ItemLoader(kHistoricOptionItem(), val)
                    loader.default_input_processor = MapCompose(unicode.strip)
                    loader.default_output_processor = Join()
                    # To iterate in item_fields dicts
                    for item, xpath in self.item_fields.iteritems():
                        loader.add_xpath(item, xpath)
                    loader.add_value("DatabaseTableName", unicode(self.databaseTableName))
                    yield loader.load_item()    
        except Exception as e:
            print e            
