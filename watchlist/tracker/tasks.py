import asyncio

from huey import crontab # SqliteHuey,
from huey.contrib.djhuey import db_periodic_task
from .services import is_market_open,get_all_stocks


@db_periodic_task(crontab(minute='*/15', hour='8-22', day_of_week='1-5'))
def get_data(): 
    try:
        market_status = is_market_open()
    except:
        print('Deu ruim na API, consagrado...')
    else:
        if (market_status.get('status') == 'open' or (market_status.get('close') > market_status.get('time'))):
            print('sim')
            get_all_stocks()        
        else:
            print('não')
            return 'market closed'

