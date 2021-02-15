import requests
import json

from datetime import timedelta, datetime
from math import trunc
from .models import post_stock


def return_not_valid(api_code):
    if trunc(api_code/100) != 2:
        raise Exception("API request had an unexpected behavior")
    return None


def time_format(value):
    datetime_format = "%Y-%m-%dT%H:%M:%SZ"

    return datetime.strptime(value, datetime_format)


def is_market_open():
    url = "https://br.financas.yahoo.com/_finance_doubledown/api/resource/finance.market-time?intl=br&lang=pt-BR&region=BR&tz=America%2FSao_Paulo&returnMeta=true"

    response = requests.get(url)

    return_not_valid(response.status_code)

    market_info = {
        "status": response.json()['data']['status'],
        "open": time_format(response.json()['data']['open']),
        "close": time_format(response.json()['data']['close']) + timedelta(hours=3),
        "time": time_format(response.json()['data']['time']),
    }

    return market_info


def get_stocks(page, size):
    crumb = "zMZ6fwKSgsB"

    url = f"https://query2.finance.yahoo.com/v1/finance/screener?crumb={crumb}&lang=en-US&region=US&formatted=true"

    payload = {"size": size, "offset": page*size, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY", "topOperator": "AND", "query": {
        "operator": "AND", "operands": [{"operator": "or", "operands": [{"operator": "EQ", "operands": ["region", "br"]}]}]}, "userId": "", "userIdType": "guid"}
    headers = {
        'Accept': '*/*',
        'Content-Type': 'application/json',
        'Cookie': 'B=5ki2645g1e347&b=3&s=qo; A1=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw; A3=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw; GUC=AQEBAgFgIhVg90IZXQN2; A1S=d=AQABBIcMF2ACEO3Xf7gB0_S70kTi8yFGSFoFEgEBAgEVImD3YB4Ab2UB_SMAAAcIhwwXYCFGSFo&S=AQAAAofS1mhrnzta8cjG8k6VzXw&j=WORLD; B=12r33u5g22cdb&b=3&s=h6; GUC=AQEBAQFgIoNgK0IZKwPa; A1=d=AQABBKsxIWACEIuN7UzFUno6jb4I0PFjbBEFEgEBAQGDImArYAAAAAAA_SMAAAcIqzEhYPFjbBE&S=AQAAAhl2lNEe3eHL9SzKQMJ_3fo; A3=d=AQABBKsxIWACEIuN7UzFUno6jb4I0PFjbBEFEgEBAQGDImArYAAAAAAA_SMAAAcIqzEhYPFjbBE&S=AQAAAhl2lNEe3eHL9SzKQMJ_3fo'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    return_not_valid(response.status_code)

    quotes = response.json()['finance']['result'][0]['quotes']

    for quote in quotes:
        code = quote['symbol'][0:-3]
        name = quote.get('longName') if quote.get(
            'longName') else quote.get('shortName')
        price = quote['regularMarketPrice']['raw']
        post_stock(code, name, price)

    return response.json()['finance']['result'][0]['total']


def get_all_stocks():
    size = 100
    response_json = get_stocks(0, size)
    pages = trunc(response_json/size)
    [get_stocks(i+1, size) for i in range(pages)]
    return 'Stocks data updated'
