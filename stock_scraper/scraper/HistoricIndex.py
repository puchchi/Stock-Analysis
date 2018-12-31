'''This module will help in automating process of 
    execution of spider and will set appropriate setting.
    You can set User Agent to random value for every 
    time spider will crawl, this will reduce chance of 
    getting banned.
'''

import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import scrapy, scraper
from scraper.spiders import HistoricIndexSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class kHistoricIndex:
    def __init__(self, stockName, startDate, endDate, databaseTableName, coldStart=True):
        self.stockName = stockName
        self.startDate = startDate
        self.endDate = endDate
        self.databaseTableName = databaseTableName
        self.codeStart = coldStart


    def __call__(self):
        # get_project_stting() will return project setting,which will be set as default setting in crawler
        process = CrawlerProcess(get_project_settings())


        # crawl will take Spider name with its *args
        process.crawl(HistoricIndexSpider.kHistoricIndexSpider, symbol=self.stockName, startDate=self.startDate, endDate=self.endDate,
                      databaseTableName=self.databaseTableName, coldStart=self.codeStart)
        # Everything is set to go and crawl.
        process.start()

class kCommand:

    def __init__(self, *args):
        self.args = args

    def run_spider(self, queue, args):
        try:
            runner = crawler.CrawlerRunner(get_project_settings())
            deferred = runner.crawl(HistoricIndexSpider.kHistoricIndexSpider, symbol=args[0][0], startDate=args[0][1], endDate=args[0][2],
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
        return "Historic Index Command"

if __name__ == "__main__":
    historicIndex = kHistoricIndex("NIFTY", "01-Jan-2018", "01-Jun-2018", "HistoricStock", True)
    historicIndex()

