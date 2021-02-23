import datetime

from django.shortcuts import render
from django.http import Http404
from django.core.exceptions import EmptyResultSet

#from rest_framework import viewsets

from .services import Watchlist
from tracker.models import get_last_stocks, get_stock_history,get_stock
#from .serializers import UserSerializer

def user_data(email):
    return Watchlist(email).validate_user()[0]


def to_dict(value):
    return {'code': value[0],
            'name': value[3],
            'price': value[1],
            'date': value[2].strftime("%Y-%m-%dT%X%Z")}


def index(request):
    user = user_data('bruno@email.com')
    stocks = get_last_stocks('name', 'date')

    content = {
        'user': user,
        'stock': list(map(to_dict, stocks))
    }
    return render(request, 'home.html', context=content)


def stock_history(request, code):
    stock = get_stock(code.upper())
    if stock is None:
        raise Http404("Stock is not listed")
    history = get_stock_history(code.upper())
    content = {
        "user": user_data('bruno@email.com'),
        "stock": stock,
        "stock_history": history
    }
    return render(request, 'stocks.html', context=content)
