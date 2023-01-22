import streamlit as st
import pandas as pd
from fbprophet import Prophet

def forecast_demand(df):
    df_prophet = df.copy()
    df_prophet = df_prophet.rename(columns={'DATE': 'ds', 'UNITS': 'y'})
    m = Prophet(weekly_seasonality=True)
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=4, freq='W')
    forecast = m.predict(future)
    return forecast

@st.experimental_memo
def Prophet_Model_loop(df):
    all_demand=pd.DataFrame()
    for i in df['ITEM'].unique():
        temp = df[df['ITEM']==i]
        demand = forecast_demand(temp)
        demand['ITEM'] = i
        demand = demand[['ITEM','ds','yhat']]
        demand = demand.rename(columns={'ds': 'DATE', 'yhat':'UNIT_FORECAST'})
        all_demand=pd.concat([all_demand, demand])
    return all_demand

if 'forecast' not in st.session_state:
    st.session_state['forecast'] = ''

if 'btn' not in st.session_state:
    st.session_state['btn'] = False

def callback1():
    st.session_state['btn'] = True


if st.session_state.df is not '':
    st.title("Demand Forecast")
    st.caption("Leverage weekly historical sales data to create a 4 weeks of demand forecast, taking into account factors such as seasonality and trends")

    df = st.session_state.df

    if st.button("Forecast Demand", on_click=callback1):
        df['DATE']= pd.to_datetime(df['DATE'])
        item_demand = Prophet_Model_loop(df) 
        st.session_state.forecast = item_demand
        

    if st.session_state.btn:
        plot_item = st.selectbox("Select an Item to Plot:", st.session_state.forecast['ITEM'].unique())
        st.line_chart(st.session_state.forecast[st.session_state.forecast['ITEM']==plot_item], x="DATE", y = ['UNIT_FORECAST'])
        st.dataframe(st.session_state.forecast[st.session_state.forecast['ITEM']==plot_item], use_container_width=True)


else:
    st.title(":orange[Upload a File under Home Tab!]")


