from queue import Queue
from threading import Thread
from django.shortcuts import render
from django.http import HttpResponse
from yahoo_fin.stock_info import *
import time 

# Create your views here.


def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, "mainapp/stockpicker.html", {'stockpicker':stock_picker})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stockpicker:
        if stock in available_stocks:
            pass
        else:
            return HttpResponse("Error")
        
    n_threads = len(stockpicker)
    thread_list = []
    que = Queue()
    start = time.time()
    print(start)
    # for stock in stockpicker:
    #     result = get_quote_table(stock)
    #     data.update({stock: result})
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
        
    for thread in thread_list:
        thread.join()
    while not que.empty():
        result = que.get()
        data.update(result)
        
    end = time.time()
    time_taken = end - start
    print(time_taken)
    return render(request, "mainapp/stocktracker.html", {'data':data})