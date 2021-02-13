from huey import crontab # SqliteHuey,
from huey.contrib.djhuey import db_periodic_task
from .services import is_market_open,get_all_stocks
from .models import get_last_stocks
from strainer.tasks import select_users


@db_periodic_task(crontab(minute='*/15', hour='8-22', day_of_week='1-5'))
def get_data(): 
    try:
        market_status = is_market_open()
    except Exception:
        print("The application is facing some issues with external API")
    else:
        if (market_status.get('status') == 'open' or (
            market_status.get('close') > market_status.get('time'))):

            print('Starting Job')
            
            get_all_stocks()  
            lastest_stock_prices = get_last_stocks()      
            select_users(lastest_stock_prices)
            return 
        else:
            print('Closed Market')
            return 'Closed Market'

