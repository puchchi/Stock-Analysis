'''This spider is used to crawl and save spot 
    value of equites like SBIN, YESBANK,    
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
from scraper.items import kHistoricEquityItem


class kHistoricEquitySpider(scrapy.Spider):
    
    name = 'kHistoricEquitySpider'
    allowed_domains = ['www.nseindia.com']
    
    def __init__(self, symbol, startDate, endDate, databaseTableName, coldStart, * args, **kwargs):
        super(kHistoricEquitySpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.databaseTableName = databaseTableName + symbol
        self.coldStart = coldStart
        

        # working_url = https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=sbin&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=01-01-2018&toDate=01-03-2018&dataType=PRICEVOLUMEDELIVERABLE
        # url = https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={symbol}&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate={startDate}&toDate={endDate}&dataType=PRICEVOLUMEDELIVERABLE
        # Referer: https://www.nseindia.com/products/content/equities/equities/eq_security.htm

    def start_requests(self):
        scrapy.Spider.start_requests(self)

        endDate = datetime.datetime.now()
        startDate = endDate - datetime.timedelta(days=3)

        if (self.coldStart == True):
            startDate =  datetime.datetime.strptime(self.startDate, "%d-%b-%Y")
            endDate = datetime.datetime.strptime(self.endDate, "%d-%b-%Y")

        while (endDate > startDate):

            tempEndDate = startDate + datetime.timedelta(days=90)

            startDateStr = startDate.strftime("%d-%m-%Y")
            tempEndDatStr = tempEndDate.strftime("%d-%m-%Y")

            url = "https://www.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=%s&segmentLink=3&symbolCount=1&series=EQ&dateRange=+&fromDate=%s&toDate=%s&dataType=PRICEVOLUMEDELIVERABLE" %(self.symbol.lower(), startDateStr, tempEndDatStr)

            yield scrapy.Request(url,self.parse, headers={'Referer': 'https://www.nseindia.com/products/content/equities/equities/eq_security.htm'})

            startDate = tempEndDate
    
    # used to save respective xpath value with their item,
    # later we can iterate through it.
    item_fields = {  
                'Date':'./td[3]//text()',
                'Open':'./td[5]//text()',
                'High':'./td[6]//text()',
                'Low':'./td[7]//text()',
                'Close':'./td[9]//text()',
                'SharesTraded':'./td[11]//text()',
                'Turnover':'./td[12]//text()'
                }
    
    def parse(self, response):
        
        # checking for response, wheather it contains records or not
        if (response.xpath("//tr[2]//text()").extract()[0].find("No Records") < 0):
            # Storing all selector except top 2(which contains waste data)
            res = response.xpath('//tr[position()>2]')
            # val will iterate from 0 to (last -1), because last res item is waste
            for val in res[0:(len(res) - 1)]:
                loader = ItemLoader(kHistoricEquityItem(), val)
                loader.default_input_processor = MapCompose(unicode.strip)
                loader.default_output_processor = Join()
                
                for item, xpath in self.item_fields.iteritems():
                    loader.add_xpath(item, xpath)
                loader.add_value('DatabaseTableName', unicode(self.databaseTableName))
                yield loader.load_item()
