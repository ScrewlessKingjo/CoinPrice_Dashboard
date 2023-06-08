import time
import streamlit as st
import altair as alt
import pandas as pd
import matplotlib.pyplot as plt
import redis
import DataHandler as DH

URL_DICT = {
    'ticker': 'https://api.bithumb.com/public/ticker/ALL_KRW',
    'orderbook': 'https://api.bithumb.com/public/orderbook/ALL_KRW'
}
HEADERS = {"accept": "application/json"}
KEY_LIST = ['BTC', 'ETC', 'XRP', 'BCH', 'QTUM', 'BTG', 'ICX', 'TRX']

rd = redis.StrictRedis(host='localhost', port=6379, db=0)
data_count = 20

st.title('코인 시세 추이')

def Load(url, headers, _rd, data_count, KEY_LIST):
    DH.DataCollector(url, headers, KEY_LIST, _rd)
    dataset = DH.DataLoader(_rd, data_count, KEY_LIST)
    return dataset

dataset = Load(URL_DICT, HEADERS, rd, data_count, KEY_LIST)

def Line_Chart(coin, data):
    chart_df = DH.ChartDataFilter(data)

    x = pd.Series(pd.to_datetime(chart_df.index)).dt.strftime('%H:%M:%S')

    bid_price = chart_df['bids']
    asks_price = chart_df['asks']

    data = pd.DataFrame({'x': x, 'bids': list(bid_price), 'asks': list(asks_price)})

    bid_scale = alt.Scale(domain=(data['bids'].min()*0.999995, data['bids'].max()*1.000005))
    asks_scale = alt.Scale(domain=(data['asks'].min()*0.999995, data['asks'].max()*1.000005))

    bid_line = alt.Chart(data).mark_line(color='blue').encode(
        x='x',
        y=alt.Y('bids', scale=bid_scale),
        tooltip=['x', 'bids']
    )
    asks_line = alt.Chart(data).mark_line(color='red').encode(
        x='x',
        y=alt.Y('asks', scale=asks_scale),
        tooltip=['x', 'asks']
    )

    chart = alt.layer(bid_line, asks_line).resolve_scale(y='independent')
    
    return chart

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader('BTC')
    BTC_Chart = Line_Chart('BTC', dataset['BTC'])
    chart_component1 = st.altair_chart(BTC_Chart, use_container_width=False)
with col2:
    st.subheader('ETC')
    ETC_Chart = Line_Chart('ETC', dataset['ETC'])
    chart_component2 = st.altair_chart(ETC_Chart, use_container_width=False)
with col3:
    st.subheader('XRP')
    XRP_Chart = Line_Chart('XRP', dataset['XRP'])
    chart_component3 = st.altair_chart(XRP_Chart, use_container_width=False)

col4, col5, col6 = st.columns(3)
with col4:
    st.subheader('BCH')
    BCH_Chart = Line_Chart('BCH', dataset['BCH'])
    chart_component4 = st.altair_chart(BCH_Chart, use_container_width=False)
with col5:
    st.subheader('QTUM')
    QTUM_Chart = Line_Chart('QTUM', dataset['QTUM'])
    chart_component5 = st.altair_chart(QTUM_Chart, use_container_width=False)
with col6:
    st.subheader('BTG')
    BTG_Chart = Line_Chart('BTG', dataset['BTG'])
    chart_component6 = st.altair_chart(BTG_Chart, use_container_width=False)

while True:
    # 데이터 업데이트
    dataset = Load(URL_DICT, HEADERS, rd, data_count, KEY_LIST)
    
    # 차트 업데이트
    chart_component1.altair_chart(Line_Chart('BTC', dataset['BTC']), use_container_width=False)
    chart_component2.altair_chart(Line_Chart('ETC', dataset['ETC']), use_container_width=False)
    chart_component3.altair_chart(Line_Chart('XRP', dataset['XRP']), use_container_width=False)
    chart_component4.altair_chart(Line_Chart('BCH', dataset['BCH']), use_container_width=False)
    chart_component5.altair_chart(Line_Chart('QTUM', dataset['QTUM']), use_container_width=False)
    chart_component6.altair_chart(Line_Chart('BTG', dataset['BTG']), use_container_width=False)
    
    time.sleep(3)  # 5초마다 업데이트