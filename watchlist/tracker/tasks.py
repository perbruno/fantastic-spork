import logging

from huey import crontab  # SqliteHuey,
from huey.contrib.djhuey import db_periodic_task
from .services import is_market_open, get_all_stocks
from .models import get_last_stocks
from strainer.tasks import select_users
from mailer.services import send_email_to


@db_periodic_task(crontab(minute='*/15', hour='8-22', day_of_week='1-5'))
def get_data():
    try:
        market_status = is_market_open()
        print(market_status)
        logging.info(market_status)
    except Exception:
        print("The application is facing some issues with external API")
    else:
        if (market_status.get('status') == 'open' or (
                market_status.get('close') > market_status.get('time'))):

            print('Starting Job')
            logging.info('Starting Job')

            get_all_stocks()
            send_email_to(select_users(get_last_stocks()))
            print('Finished')
            logging.info('Finished')
            return "Done"
        else:
            print('Closed Market')
            return 'Closed Market'
