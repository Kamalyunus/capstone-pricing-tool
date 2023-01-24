import streamlit as st
import pandas as pd
import math as m
from sklearn.linear_model import LinearRegression
import altair as alt
from altair import expr, datum

def get_elasticities(df):
    x= df.log_p.values
    y= df.log_q.values
    length = df.shape[0]
    x=x.reshape(length, 1)
    y=y.reshape(length, 1)
    reg = LinearRegression()
    reg.fit(x, y)
    return reg

@st.experimental_memo
def Elasticities_Model_loop(df):
    all_elastic=pd.DataFrame()
    for i in df['ITEM'].unique():
        temp = df[df['ITEM']==i]
        temp['log_p'] = temp.PRICE.apply(lambda x : m.log(x))
        temp['log_q'] = temp.UNITS.apply(lambda x : m.log(x))
        elastic = pd.DataFrame({'ITEM':i, 'Elasticities':[get_elasticities(temp).coef_.item()], 'Intercept':[get_elasticities(temp).intercept_.item()]})
        all_elastic=pd.concat([all_elastic, elastic])
    return all_elastic


if 'elastic' not in st.session_state:
    st.session_state['elastic'] = ''

if 'btn1' not in st.session_state:
    st.session_state['btn1'] = False

def callback1():
    st.session_state['btn1'] = True

if st.session_state.df is not '':
    st.title("Price Elasticities")
    st.caption("Leverage weekly historical sales and pricing data to estimates how changes in price will affect demand for a given item")

    df = st.session_state.df

    if st.button("Estimate Elasticities", on_click=callback1):
        item_elastic = Elasticities_Model_loop(df[['ITEM', 'UNITS', 'PRICE']]) 
        st.session_state.elastic = item_elastic
        

    if st.session_state.btn1:
        plot_item = st.selectbox("Select an Item to Plot Elasticities:", st.session_state.elastic['ITEM'].unique())
        st.dataframe(st.session_state.elastic)
        chart1 = alt.Chart(st.session_state.df[st.session_state.df['ITEM']==plot_item]).mark_circle().encode(
        x=alt.X('PRICE', scale=alt.Scale(domain=[st.session_state.df[st.session_state.df['ITEM']==plot_item].PRICE.min()-0.05, st.session_state.df[st.session_state.df['ITEM']==plot_item].PRICE.max()+0.05])),
        y=alt.Y('UNITS', title = '')
        )
        
        intercept = st.session_state.elastic[st.session_state.elastic['ITEM']==plot_item].Intercept
        beta = st.session_state.elastic[st.session_state.elastic['ITEM']==plot_item].Elasticities
        
        source=st.session_state.df[st.session_state.df['ITEM']==plot_item]
        source['CURVE'] = source['PRICE'].apply(lambda x: m.exp(intercept) * m.pow(x,beta))
        
        title = alt.TitleParams(f"PRICE ELASTICITY: {plot_item}", anchor='middle', subtitle='Orange: Estimated Price Elasticity')
        chart2 = alt.Chart(source, title = title).mark_line().encode(
        x=alt.X('PRICE', scale=alt.Scale(domain=[source.PRICE.min()-0.05, source.PRICE.max()+0.05]),axis=alt.Axis(title='PRICE', grid=False, format='$.2f')),
        y=alt.Y('CURVE', title = 'UNITS'),
        color=alt.value("#f35b04")
        )
        st.altair_chart(chart1+chart2, theme="streamlit", use_container_width=True)

else:
    st.title(":orange[Upload a File under Home Tab!]")