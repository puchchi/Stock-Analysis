'''This module will help in automating process of 
    execution of spider and will set appropriate setting.
    You can set User Agent to random value for every 
    time spider will crawl, this will reduce chance of 
    getting banned.
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scrapy, scraper, logging
from scraper.spiders import HistoricOptionSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor


class kHistoricOption:
    def __init__(self, stockName, expiries, instrumentType, databaseTableName, coldStart):
        self.stockName = stockName
        self.expiries = expiries
        self.instrumentType = instrumentType
        self.databaseTableName = databaseTableName
        self.coldStart = coldStart

    def __call__(self):
        # get_project_stting() will return project setting,which will be set as default setting in crawler
        process = CrawlerProcess(get_project_settings())
            # crawl will take Spider name with its *args
        process.crawl(HistoricOptionSpider.kHistoricOptionSpider ,symbol=self.stockName, expiries=self.expiries, instrumentType=self.instrumentType,
                      databaseTableName=self.databaseTableName, coldStart=self.coldStart)
                # Everything is set to go and crawl.
        process.start()

   
class kCommand:

    def __init__(self, *args):
        self.args = args

    def run_spider(self, queue, args):
        try:
            runner = crawler.CrawlerRunner(get_project_settings())
            deferred = runner.crawl(HistoricOptionSpider.kHistoricOptionSpider, symbol=args[0][0], expiries=args[0][1], instrumentType=args[0][2],
                                    databaseTableName=args[0][3], coldStart=args[0][-1])
            deferred.addBoth(lambda _:reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    def do(self):

        queue = Queue()
        process = Process(target=self.run_spider, args=(queue, self.args))
        process.start()
        result = queue.get()
        process.join()

        if result is not None:
            raise result

    def get_name(self):
        return "Historic Option Command"

if __name__ == "__main__":
    historicOption = kHistoricOption("SBIN", ["May2018", "Jun2018"], "OPTSTK", "HistoricOption", False)
    historicOption()

    cmd = kCommand(["SBIN", ["Jan2018", "Feb2018"], "OPTSTK", False, "HistoricOption"])
    cmd.do()
