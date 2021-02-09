import requests
import asyncio, json
import django

from datetime import timedelta,datetime
from math import trunc


def time_format(value):  
    datetime_format = "%Y-%m-%dT%H:%M:%SZ" 

    return datetime.strptime(value,datetime_format)


def is_market_open():
    url = "https://br.financas.yahoo.com/_finance_doubledown/api/resource/finance.market-time?intl=br&lang=pt-BR&region=BR&tz=America%2FSao_Paulo&returnMeta=true"

    response = requests.get(url)
    
    market_info = {
       "status" : response.json()['data']['status'],
       "open" : time_format(response.json()['data']['open']),
       "close" : time_format(response.json()['data']['close']) + timedelta(hours=3),
       "time" : time_format(response.json()['data']['time']),
    }

    return market_info 


async def get_stocks_(page, size):
    crumb = "zMZ6fwKSgsB"

    url = f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={crumb}&lang=en-US&region=US&formatted=true"

    payload={"size":size,"offset":page*size,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["region","br"]}]}]},"userId":"","userIdType":"guid"}
    headers = {
    'Accept': '*/*',
    'Content-Type': 'application/json',
    'Cookie': 'B=5ki2645g1e347&b=3&s=qo; A1=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw; A3=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw; GUC=AQEBAgFgIhVg90IZXQN2; A1S=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw&j=WORLD; B=12r33u5g22cdb&b=3&s=h6; GUC=AQEBAQFgIoNgK0IZKwPa; A1=d=AQABBKsxIWACEIuN7UzFUno6jb4I0PFjbBEFEgEBAQGDImArYAAAAAAA_SMAAAcIqzEhYPFjbBE&S=AQAAAhl2lNEe3eHL9SzKQMJ_3fo; A3=d=AQABBKsxIWACEIuN7UzFUno6jb4I0PFjbBEFEgEBAQGDImArYAAAAAAA_SMAAAcIqzEhYPFjbBE&S=AQAAAhl2lNEe3eHL9SzKQMJ_3fo'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    quotes = response.json()['finance']['result'][0]['quotes']

    for quote in quotes:
            symbol = quote['symbol'][0:-3]
            name = quote.get('longName') if quote.get('longName') else quote.get('shortName')
            quote['regularMarketPrice']['raw']


    return response.json()['finance']['result'][0]['total']


async def get_stocks():
    size = 100
    response_json = await get_stocks_(0,size)

    pages = trunc(response_json/size)

    await asyncio.gather(*[get_stocks_(i+1,size) for i in range(pages)])


def get_data():
    try:
        market_status = is_market_open()

        if (market_status.get('status') != 'open' or (market_status.get('close') > market_status.get('time'))):
            print('sim')
            asyncio.run(get_stocks())        
        else:
            print('não')
            return 'market closed'
    except:
        print('Something unexpected happened')
