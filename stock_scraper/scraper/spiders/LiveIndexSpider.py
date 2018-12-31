# This spider's url will return all the stock in that json, but we will extract only index

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import scrapy, json, datetime
from scrapy.loader import ItemLoader
from scraper.items import kLiveIndexItem

class kLiveIndexSpider(scrapy.Spider):
    
    name = 'kLiveIndexSpider'
    allowed_domains = ['www.nseindia.com']
    def __init__(self, symbol, databaseTableName, *args, **kwargs):
        super(kLiveIndexSpider, self).__init__(*args, **kwargs)
        self.symbol = symbol
        self.databaseTableName = databaseTableName
        self.timeStamp = datetime.datetime.strftime(datetime.datetime.now(), "%H%M")
        
    # working_url = https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/bankNiftyStockWatch.json
    # working_url = https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/niftyStockWatch.json
    # working_url = https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/cnxitStockWatch.json
    # working_url = https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/cnxEnergyStockWatch.json
    # referer: https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm?cat=N

    def start_requests(self):
        scrapy.Spider.start_requests(self)

        tempSymbol = ""
        if (self.symbol == "NIFTY"):
            tempSymbol = "nifty"
        elif (self.symbol == "BANKNIFTY"):
            tempSymbol = "bankNifty"
        elif (self.symbol == "CNXIT"):
            tempSymbol = "cnxit"
        elif (self.symbol == "CNXENERGY"):
            tempSymbol = "cnxEnergy"
        url = "https://www.nseindia.com/live_market/dynaContent/live_watch/stock_watch/%sStockWatch.json" %(tempSymbol)
        referer = "https://www.nseindia.com/live_market/dynaContent/live_watch/equities_stock_watch.htm?cat=N"
        request=scrapy.Request(url, self.parse,  headers={'Referer':referer})
        yield request


    def parse(self, response):
        try:
            body = response.body
            cleanedBody = body.replace('\r','').replace('\n','').replace('\t','')
            data = json.loads(cleanedBody)
            loader = ItemLoader(kLiveIndexItem())
            if len(data['data'])>0:
                latestData = data['latestData'][0]
                loader.add_value('Symbol', self.symbol)
                loader.add_value('Open', latestData['open'])
                loader.add_value('High', latestData['high'])
                loader.add_value('Low', latestData['low'])
                loader.add_value('LTP', latestData['ltp'])
                loader.add_value('TotalChange', latestData['ch'])
                loader.add_value('PerChange', latestData['per'])
                loader.add_value('Volume', data['trdVolumesum'])
                loader.add_value('Turnover', data['trdValueSum'])
                loader.add_value('DatabaseTableName', self.databaseTableName)
                loader.add_value("TimeStamp", self.timeStamp)
            return loader.load_item()                  
        except Exception as e:
            print "Error in LiveIndexSpider"
            print response.url
            print e    