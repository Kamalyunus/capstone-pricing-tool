import streamlit as st
import pandas as pd
from prophet import Prophet
import altair as alt

def forecast_demand(df):
    df_prophet = df.copy()
    df_prophet = df_prophet.rename(columns={'DATE': 'ds', 'UNITS': 'y'})
    m = Prophet()
    m.fit(df_prophet)
    future = m.make_future_dataframe(periods=4, freq='W')
    forecast = m.predict(future)
    return forecast

@st.experimental_memo
def Prophet_Model_loop(df):
    all_demand=pd.DataFrame()
    progress = 0
    my_bar = st.progress(progress)
    for i in df['ITEM'].unique():
        my_bar.progress(progress/df['ITEM'].nunique())
        temp = df[df['ITEM']==i]
        demand = forecast_demand(temp)
        demand['ITEM'] = i
        demand = demand[['ITEM','ds','yhat']]
        demand = demand.rename(columns={'ds': 'DATE', 'yhat':'UNIT_FORECAST'})
        all_demand=pd.concat([all_demand, demand])
        progress = progress + 1
    my_bar.empty()
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
        title = alt.TitleParams(f"DEMAND FORECAST: {plot_item}", anchor='middle', subtitle='Orange: Forecast     Blue: Actual')

        chart1 = alt.Chart(st.session_state.df[st.session_state.df['ITEM']==plot_item], title=title).mark_circle().encode(
        x='DATE',
        y=alt.Y('UNITS', title = '')
        )

        chart2 = alt.Chart(st.session_state.forecast[st.session_state.forecast['ITEM']==plot_item]).mark_line().encode(
        x='DATE',
        y=alt.Y('UNIT_FORECAST', title = "UNITS"),
        color=alt.value("#f35b04")
        )
        st.altair_chart(chart1+chart2, theme="streamlit", use_container_width=True)
        st.dataframe(st.session_state.forecast[st.session_state.forecast['ITEM']==plot_item], use_container_width=True)
        st.download_button(label="Download Forecast",data=st.session_state.forecast.to_csv(index=False).encode('utf-8'),file_name='demand_forecast.csv',mime='text/csv',)



else:
    st.title(":orange[Upload a File under Home Tab!]")


