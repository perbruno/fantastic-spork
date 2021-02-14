from watchlist.tracker.models import Stock
from .models import User
from .services import Radar


def get_interested_users(action,quotes):
    for stock,price in quotes:
        users = User.objects.filter(watchlist__has_key = stock)\
            .values('email','watchlist','radar')
        for user in users:

            if bool(user['watchlist'][stock].get(action) is not None) and \
                (bool(action=='buy' and user['watchlist'][stock].get(action)>=price) ^ \
                bool(action=='sell' and user['watchlist'][stock].get(action)<=price)):

                Radar.add_item(user['email'], stock,action,price)

            elif bool(type(user['radar'])==dict) and \
                (bool(action=='buy' and user['watchlist'][stock].get(action)<price) ^ \
                bool(action=='sell' and user['watchlist'][stock].get(action)>price)):

                Radar.delet_item(user['email'], stock,action,price)

            
    return None


def select_users(lastest_stock_prices):
    get_interested_users('buy',lastest_stock_prices)
    get_interested_users('sell',lastest_stock_prices)