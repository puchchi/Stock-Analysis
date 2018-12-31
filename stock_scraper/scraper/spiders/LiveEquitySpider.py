import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import scrapy, json, datetime
from scrapy.loader import ItemLoader
from scraper.items import kLiveEquityItem

class kLiveEquitySpider(scrapy.Spider):
    
    name = 'kLiveEquitySpider'
    allowed_domains = ['www.nseindia.com']
    def __init__(self, symbol, databaseTableName, *args, **kwargs):
        super(kLiveEquitySpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.databaseTableName = databaseTableName
        self.timeStamp = datetime.datetime.strftime(datetime.datetime.now(), "%H%M")
        
    # working_url = https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=SBIN
    # referer: https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=SBIN

    def start_requests(self):
        scrapy.Spider.start_requests(self)

        url = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/ajaxGetQuoteJSON.jsp?symbol=%s" %(self.symbol)
        referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=%s" %(self.symbol)
        request=scrapy.Request(url, self.parse,  headers={'Referer':referer})
        yield request


    def parse(self, response):
        try:
            body = response.body
            cleanedBody = body.replace('\r','').replace('\n','').replace('\t','')
            data = json.loads(cleanedBody)
            loader = ItemLoader(kLiveEquityItem())
            if len(data['data'])>0:
                data = data['data'][0]
                loader.add_value('Symbol', self.symbol)
                loader.add_value('Open', data['open'])
                loader.add_value('High', data['dayHigh'])
                loader.add_value('Low', data['dayLow'])
                #loader.add_value('PrevClose', data['previousClose'])
                loader.add_value('LTP', data['lastPrice'])
                loader.add_value('TotalChange', data['change'])
                loader.add_value('PerChange', data['pChange'])
                loader.add_value('Volume', data['totalTradedVolume'])
                loader.add_value('Turnover', data['totalTradedValue'])
                #loader.add_value('TotalBuyQuantity', data['totalBuyQuantity'])
                #loader.add_value('TotalSellQuantity', data['totalSellQuantity'])
                loader.add_value('DatabaseTableName', self.databaseTableName)
                loader.add_value("TimeStamp", self.timeStamp)
            return loader.load_item()                  
        except Exception as e:
            print "Error in LiveEquitySpider"
            print response.url
            print e    