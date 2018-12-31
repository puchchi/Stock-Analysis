import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import scrapy, json, datetime
from scrapy.loader import ItemLoader
from scraper.items import kLiveFutureItem

class kLiveFutureSpider(scrapy.Spider):
    
    name = 'kLiveFutureSpider'
    allowed_domains = ['www.nseindia.com']
    def __init__(self, executerInstance, *args, **kwargs):
        super(kLiveFutureSpider, self).__init__(*args, **kwargs)
        self.executerInstance = executerInstance
        LiveFutureSpider.start_urls = self.executerInstance.startURL
        
    def getStockIdentifier(self, underlying, expiry):
        expiryCode = datetime.datetime.strptime(expiry, '%d%b%Y').strftime('%y%m')
        return self.executerInstance.stockToId[underlying]*10000 + int(expiryCode)
        
    def parse(self, response):
        try:
            body = response.body
            cleanedBody = body.replace('\r','').replace('\n','').replace('\t','')
            data = json.loads(cleanedBody)
            loader = ItemLoader(kLiveFutureItem())
            if len(data['data'])>0:
                data = data['data'][0]
                loader.add_value('StockIdentifier_f', unicode(self.getStockIdentifier(data['underlying'], data['expiryDate'])))
                loader.add_value('Open', data['openPrice'])
                loader.add_value('High', data['highPrice'])
                loader.add_value('Low', data['lowPrice'])
                loader.add_value('PrevClose', data['prevClose'])
                loader.add_value('LastTradedPrice', data['lastPrice'])
                loader.add_value('Volume', data['numberOfContractsTraded'])
                loader.add_value('Turnover', data['turnoverinRsLakhs'])
                loader.add_value('UnderlyingValue', data['underlyingValue'])
                loader.add_value('AnnualisedVolatility', data['annualisedVolatility'])
                loader.add_value('DailyVolatility', data['dailyVolatility'])
                loader.add_value('OpenInterest', data['openInterest'])
                loader.add_value('ChangeInOI', data['changeinOpenInterest'])
                loader.add_value('PerChangeInOI', data['pchangeinOpenInterest'])
            return loader.load_item()                  
        except Exception as e:
            print "Error in LiveFutureSpdier"
            print response.url
            print e    