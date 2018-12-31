import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import thread
import datetime
import time

from scraper import utility, AutoLiveOptionValue

class kInfiniteRunningTask:
    def __init__(self, task, timeLowerBound, timeUpperBound, isTimeStamp, * args):
        self.task = task
        self.timeLowerBound = timeLowerBound
        self.timeUpperBound = timeUpperBound
        self.isTimeStamp = isTimeStamp
        #self.args[] = args

    def do(self):
        thread.start_new_thread(self.doThreading(), [])

    def doThreading(self):
        if (self.isTimeStamp):
            timeStamp = self.timeLowerBound
            while timeStamp < self.timeUpperBound:
                timeStamp = int(datetime.datetime.strftime(datetime.datetime.now(), "%H%M"))
                thread.start_new_thread(self.doingNow(), [])
                time.sleep(30)

    def doingNow(self):
        autoLiveOptionValue = AutoLiveOptionValue.kAutoLiveOptionValue(utility.stockName)
        #thread.start_new_thread(autoLiveOptionValue.do(), [])
        autoLiveOptionValue.do()
