import datetime
import requests
import json
import time
import numpy as np
import pandas as pd
import redis

URL_DICT = {
'ticker': 'https://api.bithumb.com/public/ticker/ALL_KRW',
'orderbook': 'https://api.bithumb.com/public/orderbook/ALL_KRW'}
HEADERS = {"accept": "application/json"}
KEY_LIST = ['BTC', 'ETC', 'XRP', 'BCH', 'QTUM', 'BTG']


rd = redis.StrictRedis(host='localhost', port=6379, db=0)

def OrderbookDataCollector(url, headers,key_list):
    result_dict = {}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)['data']

    for key in key_list :
        bid_list = []
        asks_list = []
        
        for count in data[key]['bids']:
            bid_list.append(float(count['price']))
        
        for count in data[key]['asks']:
            asks_list.append(float(count['price']))
            
        result_dict[key] = {'bids' : int(np.round(sum(bid_list)/len(bid_list), 0)),
            'asks' : int(np.round(sum(asks_list)/len(asks_list), 0))}      
        
    
    return result_dict


def DataCollector(url, headers,key_list, rd) :
    
    result_dict = {}
    response = requests.get(url['ticker'], headers=headers)
    data = json.loads(response.text)['data']
    unix_time = int(data['date']) / 1000
    datekey = datetime.datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S')
    
    for key in key_list : 
        result_dict[key] = data[key]


    orderbook_data = OrderbookDataCollector(url['orderbook'], headers, key_list)
    
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
    temp_dict = {}
    for key in sorted_keys[:count]:
        value = redis_client.get(key)
        temp_dict[key.decode()] = json.loads(value.decode())
    
    return temp_dict


def DataFrameGenerator(result, key_list):
    result_dict = {}

    for coin in key_list:
        df_list = []
        for dict_key in result.keys():
            df_list.append(result[dict_key][coin])
        df = pd.DataFrame(df_list, index=result.keys())
        result_dict[coin] = df

    return result_dict

def DataLoader(rd, data_count, KEY_LIST):
    data_list = GetLatestData(rd, data_count)
    df_dict = DataFrameGenerator(data_list, KEY_LIST)

    return df_dict


def ChartDataFilter(df):
    
    columns_keep = ['min_price', 'max_price', 'bids', 'asks']
    columns_drop = [col for col in df.columns if col not in columns_keep]
    
    df_filtered = df.drop(columns_drop, axis=1)
    
    return df_filtered[::-1]


def TableDataFilter(df_dict) : 
    index = ['시가', '종가', '저가', '고가', '거래량', '거래금액', '전일종가', '최근 1일 거래량', '최근 1일 거래금액', '최근 1일 변동가', '최근 1일 변동률', '최신 매수가', '최신 매도가']
    for coin in df_dict.keys():
        df = pd.DataFrame(df_dict[coin])
        df.index= index

    return df


if __name__ == "__main__":
    for i in range(100) :
       DataCollector(URL_DICT, HEADERS, KEY_LIST, rd)
       time.sleep(5)