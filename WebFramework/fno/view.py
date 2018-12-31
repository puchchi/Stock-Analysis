import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(path.dirname(path.abspath(__file__)))

import simplejson, MySQLdb, datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from fno.forms import kOptionValueForm
from fno.views import IndexView, StockOIView

def index(request):
    indexView = IndexView.kView(request)
    return indexView()

def totalCallPut(request, arg):
    assert isinstance(request, HttpRequest)
    
    # tablename in db is like OptionValueOfNiftyMar2018
    tableName = "OptionValueOf" + arg[0] + arg[1] + arg[2]
    ceResult = []
    peResult = []
    try:
        db = MySQLdb.connect('localhost', 'StockUser', 'StockPass', 'StockDB', charset="utf8", use_unicode=True)
        cursor = db.cursor()
        sqlCE = '''select date, sum(OpenInterest) from %s  where optiontype="CE" group by date;''' %(tableName)
        sqlPE = '''select date, sum(OpenInterest) from %s  where optiontype="PE" group by date;''' %(tableName)

        cursor.execute(sqlCE)
        ceResult = cursor.fetchall()

        cursor.execute(sqlPE)
        peResult = cursor.fetchall()

        cursor.close()
    except:
        print "Error executing SQL in option views.py"

    dict = [['Date', 'CE OI', 'PE OI']]
    for i in range(len(ceResult)):
        #will convert 20180129L to 01-Jan-2018
        date = datetime.datetime.strptime(str(ceResult[i][0]), "%Y%m%d").strftime("%d-%b-%Y")
        ceOpenInterest = int(ceResult[i][1])
        peOpenInterest = int(peResult[i][1])
        dict.insert(len(dict), [date, ceOpenInterest, peOpenInterest])
    print dict
    #dict=[['Date', 'CE OI', 'PE OI', 'Nifty'], ['01-Dec-2017', 41325, 9375, 10121.8], ['04-Dec-2017', 63450, 84300, 10127.8], ['05-Dec-2017', 87075, 149625, 10118.2], ['06-Dec-2017', 162600, 174900, 10044.1], ['07-Dec-2017', 225750, 246825, 10166.7], ['08-Dec-2017', 270900, 317400, 10265.7], ['11-Dec-2017', 315075, 353925, 10322.2], ['12-Dec-2017', 347025, 377325, 10240.2], ['13-Dec-2017', 366675, 413250, 10193.0], ['14-Dec-2017', 459150, 760200, 10252.1], ['15-Dec-2017', 601050, 867375, 10333.2], ['18-Dec-2017', 662850, 985200, 10388.8], ['19-Dec-2017', 751650, 1242300, 10463.2], ['20-Dec-2017', 906450, 1618275, 10444.2], ['21-Dec-2017', 1009800, 1880325, 10440.3], ['22-Dec-2017', 1108500, 2117700, 10493.0], ['26-Dec-2017', 1201575, 2334300, 10531.5], ['27-Dec-2017', 1307850, 3409275, 10490.8], ['28-Dec-2017', 1486050, 3972825, 10477.9], ['29-Dec-2017', 1983225, 4972875, 10530.7], ['01-Jan-2018', 2122575, 5968050, 10435.5], ['02-Jan-2018', 2583525, 6098775, 10442.2], ['03-Jan-2018', 2828250, 6396900, 10443.2], ['04-Jan-2018', 3125025, 6612825, 10504.8], ['05-Jan-2018', 3543675, 7045800, 10558.8], ['08-Jan-2018', 4076025, 7868700, 10623.6]]
    js_data = simplejson.dumps(dict)

    my_dict = {'oi':js_data}

    return render(
        request,
        'option/oi.html', my_dict
    )

def stockView(request):

    stockView = StockOIView.kView(request)
    return stockView()



