import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import simplejson, MySQLdb, datetime

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from fno.forms import kOptionValueForm
from fno.views import StockOIView

class kView:

    def __init__(self, request):
        self.request = request

    def __call__(self):
        if self.request.method == 'POST':
            form = kOptionValueForm(self.request.POST)
            if form.is_valid():
                #print form
                stockOIView = StockOIView.kView(self.request)
                return stockOIView()
            else:
                print form.errors
        else:
            form = kOptionValueForm()
    
        return render(self.request, 'fno/index.html', {'form':form})