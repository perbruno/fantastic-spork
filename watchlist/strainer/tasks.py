from watchlist.tracker.models import Stock
from .models import User
from .services import Radar, check_crossed_borders


def get_interested_users(action, quotes):
    userlist = set()
    for stock, price in quotes:
        users = User.objects.filter(watchlist__has_key=stock)\
            .values('email', 'watchlist', 'radar')
        for user in users:
            if check_crossed_borders('outside', action, stock, price, user):
                Radar.add_item(user['email'], stock, action)
                userlist.add(user['email'])
            elif check_crossed_borders('inside', action, stock, price, user):
                Radar.delete_item(user['email'], stock, action, price)
                userlist.add(user['email'])
    return userlist


def select_users(lastest_stock_prices):
    buyers = get_interested_users('buy', lastest_stock_prices)
    sellers = get_interested_users('sell', lastest_stock_prices)
    selected_users = list(set(buyers) | set(sellers))
    return selected_users
