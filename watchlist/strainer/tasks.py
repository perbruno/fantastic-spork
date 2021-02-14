from tracker.models import Stock
from .models import User
from .services import Radar


def get_interested_users(action,quotes):
    for stock,price in quotes:
        users = User.objects.filter(watchlist__has_key = stock)\
            .values('email','watchlist','radar')
        if len(users) == 0:
            continue
        elif action=='buy':
            for user in users:
                if user['watchlist'][stock].get(action) is not None:
                    # if user['radar'].get(action).get(stock)
                    if user['watchlist'][stock].get(action)>=price:
                        #  Radar.add_item(user.email, action,stock):

                    else:
                else:
                    continue
            pass
        else:
            pass

    # user , action , stock
    pass


def select_users(lastest_stock_prices):
    buyers = get_interested_users('buy',lastest_stock_prices)
    sellers = get_interested_users('sell',lastest_stock_prices)
    check_radar(buyers, sellers)