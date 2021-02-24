import ast

from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

from .services import Watchlist
from .forms import WatchlistForm
from .models import User
from tracker.models import get_last_stocks, get_stock_history, get_stock


def user_data(email='bruno@email.com'):
    return Watchlist(email).validate_user()[0]


def to_dict(value):
    return {'code': value[0],
            'name': value[3],
            'price': value[1],
            'date': value[2].strftime("%Y-%m-%dT%X%Z")}


@ensure_csrf_cookie
def index(request):
    user = user_data()
    stocks = get_last_stocks('name', 'date')

    WatchlistForm(instance=User.objects.get(pk='bruno@email.com'))

    content = {
        'user': user,
        'stock': list(map(to_dict, stocks)),
        'form': WatchlistForm(instance=User.objects.get(pk='bruno@email.com'))
    }
    return render(request, 'home.html', context=content)


@ensure_csrf_cookie
def stock_history(request, code):
    stock = get_stock(code.upper())
    if stock is None:
        raise Http404("Stock is not listed")
    history = get_stock_history(code.upper())
    content = {
        "user": user_data(),
        "stock": stock,
        "stock_history": history,
        "form": WatchlistForm(instance=User.objects.get(pk='bruno@email.com'))
    }
    return render(request, 'stocks.html', context=content)


@ensure_csrf_cookie
def watchlist_form(request, user):
    if request.method == 'POST':
        form = ast.literal_eval(request.POST['watchlist'])
        data = User.objects.get(email=user)
        data.watchlist = form
        data.save()
    return HttpResponseRedirect('/')
