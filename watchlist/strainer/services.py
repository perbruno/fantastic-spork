import pytz

from datetime import datetime
from django.db import models

from .models import User
# from watchlist.tracker.models import get_stock


class Watchlist:
    def __init__(self, email):
        self.email = email

    def validate_user(self):
        try:
            user_data = User.objects.filter(email__exact=self.email).values()
        except models.EmptyResultSet as err:
            print("User {} doesn't exist.{}".format(self.email, err))
        else:
            return user_data

    def get_watchlist(self):
        user_data = self.validate_user()
        watchlist = user_data.first().get('watchlist')
        return watchlist if watchlist != '{}' else "User's watchlist is empty"

    def post_watchlist(self, **kwargs):
        """
        the following model must be respected:
            user.post_watchlist(code = {'buy': 00.00 , 'sell':10.00} ...)
        """
        self.validate_user()

        return kwargs

    def put_watchlist(self, **kwargs):
        """
        the following model must be respected:
            user.put_watchlist(code = {'buy': 00.00 , 'sell':10.00} ...)
        """
        self.validate_user()
        pass

    def delete_watchlist(self, **kwargs):
        self.validate_user()
        pass


class Radar:
    def __init__(self):
        super().__init__()

    @staticmethod
    def check_radar(user, action, stock):
        if type(user['radar']) == dict and \
                user['radar'].get(action) is not None and \
                stock in user['radar'][action]:
            return True
        else:
            return False

    @staticmethod
    def save_radar(user):
        User.objects.filter(email__exact=user['email'])\
                    .update(radar=user['radar'],
                            updated_at=datetime.now(tz=pytz.UTC))
        return None

    @classmethod
    def add_item(cls, user, stock, action):
        if type(user['radar']) == dict:
            if user['radar'].get(action) is not None:
                user['radar'].get(action).append(stock)
            else:
                user['radar'].update({action: [stock]})
        else:
            user['radar'] = {action: [stock]}
        Radar.save_radar(user)

    @staticmethod
    def delete_item(user, stock, action):
        user['radar'].get(action).remove(stock)
        Radar.save_radar(user)


def check_crossed_borders(direction, action, stock, price, user):
    if user['watchlist'][stock].get(action) is None:
        return False
    else:
        if direction == 'outside' and not Radar.check_radar(user, action, stock) and \
            (action == 'buy' and user['watchlist'][stock].get(action) >= price) ^ \
                (action == 'sell' and user['watchlist'][stock].get(action) <= price):
            return True
        elif direction == 'inside' and Radar.check_radar(user, action, stock) and \
            (action == 'buy' and user['watchlist'][stock].get(action) < price) ^ \
                (action == 'sell' and user['watchlist'][stock].get(action) > price):
            return True
        else:
            return False
