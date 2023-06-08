import time
import streamlit as st
import altair as alt
import pandas as pd
import redis
import DataHandler as DH

URL_DICT = {
    'ticker': 'https://api.bithumb.com/public/ticker/ALL_KRW',
    'orderbook': 'https://api.bithumb.com/public/orderbook/ALL_KRW'
}
HEADERS = {"accept": "application/json"}
KEY_LIST = ['BTC', 'ETC', 'XRP', 'BCH', 'QTUM', 'BTG']

rd = redis.StrictRedis(host='localhost', port=6379, db=0)
data_count = 15


def Load(url, headers, _rd, data_count, KEY_LIST):
    DH.DataCollector(url, headers, KEY_LIST, _rd)
    dataset = DH.DataLoader(_rd, data_count, KEY_LIST)
    return dataset



def Line_Chart(data):
    chart_df = DH.ChartDataFilter(data)

    x = pd.Series(pd.to_datetime(chart_df.index)).dt.strftime('%H:%M:%S')

    bid_price = chart_df['bids']
    asks_price = chart_df['asks']

    data = pd.DataFrame({'x': x, 'bids': list(bid_price), 'asks': list(asks_price)})

    bid_scale = alt.Scale(domain=(data['bids'].min()*0.999995, data['bids'].max()*1.000005))
    asks_scale = alt.Scale(domain=(data['asks'].min()*0.999995, data['asks'].max()*1.000005))

    bid_line = alt.Chart(data).mark_line(color='blue').encode(
        x=alt.X('x', axis=alt.Axis(title='시간')),
        y=alt.Y('bids', scale=bid_scale, axis=alt.Axis(title='가격')),
        tooltip=['x', 'bids'])
    
    asks_line = alt.Chart(data).mark_line(color='red').encode(
        x=alt.X('x', axis=alt.Axis(title='시간')),
        y=alt.Y('asks', scale=asks_scale, axis=alt.Axis(title='가격')),
        tooltip=['x', 'asks'])

    chart = alt.layer(bid_line, asks_line).resolve_scale(y='independent')
    
    return chart

st.set_page_config(layout="wide")
st.title('가상화폐 시세 추이')

with st.container():
    table = st.empty()


dataset = Load(URL_DICT, HEADERS, rd, data_count, KEY_LIST)

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('BTC')
    BTC_Chart = Line_Chart(dataset['BTC'])
    chart_component1 = st.altair_chart(BTC_Chart, use_container_width=True)

with col2:
    st.subheader('ETC')
    ETC_Chart = Line_Chart(dataset['ETC'])
    chart_component2 = st.altair_chart(ETC_Chart, use_container_width=True)

with col3:
    st.subheader('XRP')
    XRP_Chart = Line_Chart(dataset['XRP'])
    chart_component3 = st.altair_chart(XRP_Chart, use_container_width=True)

col4, col5, col6 = st.columns(3)

with col4:
    st.subheader('BCH')
    BCH_Chart = Line_Chart(dataset['BCH'])
    chart_component4 = st.altair_chart(BCH_Chart, use_container_width=True)

with col5:
    st.subheader('QTUM')
    QTUM_Chart = Line_Chart(dataset['QTUM'])
    chart_component5 = st.altair_chart(QTUM_Chart, use_container_width=True)

with col6:
    st.subheader('BTG')
    BTG_Chart = Line_Chart(dataset['BTG'])
    chart_component6 = st.altair_chart(BTG_Chart, use_container_width=True)


while True:
    dataset = Load(URL_DICT, HEADERS, rd, data_count, KEY_LIST)
    
    chart_component1.altair_chart(Line_Chart(dataset['BTC']), use_container_width=True)
    chart_component2.altair_chart(Line_Chart(dataset['ETC']), use_container_width=True)
    chart_component3.altair_chart(Line_Chart(dataset['XRP']), use_container_width=True)
    chart_component4.altair_chart(Line_Chart(dataset['BCH']), use_container_width=True)
    chart_component5.altair_chart(Line_Chart(dataset['QTUM']), use_container_width=True)
    chart_component6.altair_chart(Line_Chart(dataset['BTG']), use_container_width=True)
    table_dataset  = DH.GetLatestData(rd, 1)
    table_data = DH.TableDataFilter(table_dataset)
    table.dataframe(table_data.astype(str), width=2200, height=512, use_container_width=True)
    time.sleep(3)