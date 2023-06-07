import requests
import json
import datetime
import numpy as np
import pandas as pd
import redis

URL_DICT = {
'ticker': 'https://api.bithumb.com/public/ticker/ALL_KRW',
'orderbook': 'https://api.bithumb.com/public/orderbook/ALL_KRW'}
HEADERS = {"accept": "application/json"}
KEY_LIST = ['BTC', 'ETC', 'XRP', 'BCH', 'QTUM', 'BTG', 'ICX', 'TRX']


rd = redis.StrictRedis(host='localhost', port=6379, db=0)

def OrderbookDataCollector(url, headers,key_list, rd):
    result_dict = {}
    response = requests.get(url, headers=HEADERS)
    data = json.loads(response.text)['data']

    for key in key_list :
        bid_list = []
        asks_list = []
        
        for count in data[key]['bids']:
            bid_list.append(float(count['price']))
        
        for count in data[key]['asks']:
            asks_list.append(float(count['price']))
            
        result_dict[key] = {'bids' : np.round(sum(bid_list)/len(bid_list), 2),
            'asks' : np.round(sum(asks_list)/len(asks_list), 2)}      
        
    
    return result_dict


def DataCollector(url, headers,key_list, rd) :
    
    result_dict = {}
    response = requests.get(url['ticker'], headers=headers)
    data = json.loads(response.text)['data']
    unix_time = int(data['date']) / 1000
    datekey = datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    
    for key in key_list : 
        result_dict[key] = data[key]


    orderbook_data = OrderbookDataCollector(url['orderbook'], headers, key_list, rd)
    
    combined_dict = {
        currency: {
            **values,
            'bids': orderbook_data[currency]['bids'],
            'asks': orderbook_data[currency]['asks']
        }
        for currency, values in result_dict.items()
    }
    jsonDataDict = json.dumps(combined_dict, ensure_ascii=False).encode('utf-8')
    rd.set(datekey, jsonDataDict)

    return None

def GetLatestData(redis_client, count):
    keys = redis_client.keys()
    sorted_keys = sorted(keys, reverse=True)  
    latest_data = []
    
    for key in sorted_keys[:count]:
        value = redis_client.get(key)
        latest_data.append({key.decode(): value.decode()})
    
    return latest_data


def DataFrameGenerator(result, coin) : 
    df_list = []
    for dict_key in result.keys() :
        df_list.append(result[dict_key][coin])
    df=pd.DataFrame(df_list, index=result.keys())
    return df


# DataCollector(URL_DICT, HEADERS, KEY_LIST, rd)