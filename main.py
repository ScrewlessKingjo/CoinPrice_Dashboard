import streamlit as st
import pandas as pd
import DataHandler as DH

URL_DICT = {
'ticker': 'https://api.bithumb.com/public/ticker/ALL_KRW',
'orderbook': 'https://api.bithumb.com/public/orderbook/ALL_KRW'}
HEADERS = {"accept": "application/json"}
KEY_LIST = ['BTC', 'ETC', 'XRP', 'BCH', 'QTUM', 'BTG', 'ICX', 'TRX']

st.title('Hello Streamlit')

while True : 
    DH.DataCollector(URL_DICT, HEADERS, KEY_LIST)
    

