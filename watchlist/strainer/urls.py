from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('stock/<str:code>', views.stock_history, name='stock-history'),
    path('user/<str:user>/watchlist', views.watchlist_form, name='watchlist-form'),
]
