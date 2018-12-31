'''This spider is used to crawl and save spot 
    value of indices like NIFTY 50, BANKNIFTY,    
    etc. You need to provide SYMBOL, STARTDATE,
    & ENDDATE as argument to this spider.
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import datetime
import scrapy, scraper
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import Join, MapCompose
from scraper.items import kHistoricIndexItem
from scraper import utility


class kHistoricIndexSpider(scrapy.Spider):
    
    name = 'kHistoricIndexSpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, startDate, endDate, databaseTableName, coldStart, * args, **kwargs):
        super(kHistoricIndexSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.databaseTableName = databaseTableName + symbol
        self.coldStart = coldStart

        # working url = https://www.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=NIFTY%20BANK&fromDate=01-Jan-2010&toDate=01-Mar-2010
    

    def start_requests(self):
        scrapy.Spider.start_requests(self)
        
        symbol = ""
        if (self.symbol == "NIFTY"):
            symbol = "NIFTY 50"
        elif (self.symbol == "BANKNIFTY"):
            symbol = "NIFTY BANK"
        else:
            print "CRITICAL_ERROR Symbol not found in HistoricIndexSpider"

        endDate = datetime.datetime.now()
        startDate = endDate - datetime.timedelta(days=3)

        if (self.coldStart == True):
            startDate =  datetime.datetime.strptime(self.startDate, "%d-%b-%Y")
            endDate = datetime.datetime.strptime(self.endDate, "%d-%b-%Y")

        while (endDate > startDate):

            tempEndDate = startDate + datetime.timedelta(days=90)

            forceBreak = False
            if tempEndDate >= datetime.datetime.now():
                tempEndDate = datetime.datetime.now() - datetime.timedelta(days=1)
                forceBreak = True

            startDateStr = startDate.strftime("%d-%b-%Y")
            tempEndDatStr = tempEndDate.strftime("%d-%b-%Y")

            url = "https://www.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp?indexType=%s&fromDate=%s&toDate=%s" %(symbol, startDateStr, tempEndDatStr)
            yield scrapy.Request(url,self.parse)

            startDate = tempEndDate

            if forceBreak:
                break

   
    # used to save respective xpath value with their item,
    # later we can iterate through it.
    item_fields = {  
                'Date':'./td[1]//text()',
                'Open':'./td[2]//text()',
                'High':'./td[3]//text()',
                'Low':'./td[4]//text()',
                'Close':'./td[5]//text()',
                'SharesTraded':'./td[6]//text()',
                'Turnover':'./td[7]//text()'
                }
    
    def parse(self, response):
        
        # checking for response, wheather it contains records or not
        if ((response.xpath("//tr[3]//text()").extract()[0].find("No Records") < 0)):
              
            # Storing all selector except top 3(which contains waste data)
            res = response.xpath('//tr[position()>3]')
            # val will iterate from 0 to (last -1), because last res item is waste
            for val in res[0:len(res)]:
                loader = ItemLoader(kHistoricIndexItem(), val)
                loader.default_input_processor = MapCompose(unicode.strip)
                loader.default_output_processor = Join()
                
                for item, xpath in self.item_fields.iteritems():
                    loader.add_xpath(item, xpath)
                loader.add_value('DatabaseTableName', unicode(self.databaseTableName))
                yield loader.load_item()
