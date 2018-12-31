import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import datetime
import scrapy, scraper.spiders, logging
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scraper import utility
from scraper.items import kLiveOptionItem
from scrapy.loader.processors import Join, MapCompose


class kLiveOptionSpider(scrapy.Spider):
    
    name = 'kLiveOptionSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, instrumentType, databaseTableName, expiries=[], * args, **kwargs):
        super(kLiveOptionSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.expiries = expiries
        self.instrumentType = instrumentType
        self.databaseTableName = databaseTableName
        self.timeStamp = datetime.datetime.strftime(datetime.datetime.now(), "%H%M")
        
    def start_requests(self):
        scrapy.Spider.start_requests(self)    

        for expiry in self.expiries:
            temp = datetime.datetime.strptime(expiry, "%b%Y")   # Expiry are in "Jan2018" format.
            month = temp.month
            year = temp.year
            expiryDate = utility.indexExpiryDate[year][month-1]
            expiryDateStd = datetime.datetime.strptime(expiryDate, "%d-%m-%Y")
            expiryDate = expiryDateStd.strftime("%d%b%Y").upper()
            dateList = [expiryDateStd - datetime.timedelta(days=x) for x in range(0, utility.daysBetweenExpiry)]

            for date in dateList:
                standardDate = date.strftime("%d-%b-%Y")
                url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=&instrument=%s&symbol=%s&date=%s" %(self.instrumentType, self.symbol, expiryDate)
                request=scrapy.Request(url, self.parse,  headers={'Referer':'https://www.nseindia.com/products/content/derivatives/equities/historical_fo.htm'})
                yield request

        #Working URL
        # https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=SBIN
        #https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=17&instrument=OPTSTK&symbol=SBIN&date=26JUL2018

        #url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=%s" %(self.symbol)
        #url = "https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?segmentLink=&instrument=%s&symbol=%s&date=%s" %(self.
        #request=scrapy.Request(url, self.parse)
        #yield request

    
    item_fields = {
                'OpenInterestCall':'./td[2]//text()',
                'ChangeInOICall':'./td[3]//text()',
                'VolumeCall':'./td[4]//text()',
                'ImpliedVolatilityCall':'./td[5]//text()',
                'LTPCall':'./td[6]//text()',
                'NetChangeCall':'./td[7]//text()',
                'StrikePrice':'./td[12]//text()',
                'NetChangePut':'./td[17]//text()',
                'LTPPut':'./td[18]//text()',
                'ImpliedVolatilityPut':'./td[19]//text()',
                'VolumePut':'./td[20]//text()',
                'ChangeInOIPut':'./td[21]//text()',
                'OpenInterestPut':'./td[22]//text()',
                 }
    
    def parse(self, response):
        try:
            #print response.url
            responseUrl = response.url
            expiry = responseUrl.split("date=")[1]
            expiry = expiry[2:]
            res = response.xpath('//table[@id="octable"]/tr')
            for val in res[0:(len(res) - 1)]:
                loader = ItemLoader(kLiveOptionItem(), val)
                loader.default_output_processor = Join()
                for item, xpath in self.item_fields.iteritems():
                    loader.add_xpath(item, xpath)
                loader.add_value("DatabaseTableName", self.databaseTableName)
                loader.add_value("Symbol", self.symbol)
                loader.add_value("Expiry", expiry)
                loader.add_value("TimeStamp", self.timeStamp)
                yield loader.load_item()
        except Exception as e:
            print "Error in kLiveOptionValueSpider"
            print e
 
