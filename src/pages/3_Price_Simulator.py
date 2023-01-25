import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

@st.experimental_memo
def simulate(x, e, bp, bq):
    perc_qty_change = np.multiply(e,x)
    new_price = bp + np.multiply(bp,x)
    new_qty = bq + np.multiply(perc_qty_change,bq)
    sim_revenue = np.dot(new_price, new_qty)
    baseline_revenue = np.dot(bp,bq)
    baseline_qty=sum(bq)
    sim_qty=sum(new_qty)
    lm = bp - new_price
    investment = np.dot(lm,bq)
    return [baseline_revenue, sim_revenue, baseline_qty, sim_qty, investment, new_price]


if 'btn2' not in st.session_state:
    st.session_state['btn2'] = False

if 'sim' not in st.session_state:
    st.session_state.sim = ''

if 'user_p' not in st.session_state:
    st.session_state.user_p = ''

def callback1():
    st.session_state['btn2'] = True

if st.session_state.df is not '' and st.session_state.elastic is not '' and st.session_state.forecast is not '':

    st.title("Simulation Results")  

    df = st.session_state.df


    e = st.session_state.elastic['Elasticities'].to_numpy()
    bp = df.loc[df.groupby(["ITEM"])["DATE"].idxmax()].PRICE.to_numpy()   
    bq = st.session_state.forecast.groupby("ITEM").tail(4).groupby("ITEM")["UNIT_FORECAST"].sum().to_numpy()
    num_items = e.size 

    if st.session_state.user_p == '':
        max_price = st.sidebar.slider("Price Reduction for All Items:",0,50,20, step=5, help = "Price Reduction per Item ", format="%d%%")
    else:
        max_price = st.sidebar.slider("Price Reduction for All Items:",0,50,st.session_state.user_p, step=5, help = "Price Reduction per Item ", format="%d%%")
    

    if st.sidebar.button("Calculate", on_click=callback1):
        with st.spinner("Please Wait..."):
            user_price = np.ones(num_items)*(max_price/100)
            st.session_state.sim = simulate(-user_price,e,bp,bq) 
            st.session_state.user_p = max_price
            
    if st.session_state.btn2:
        panel1=st.container()
        panel2=st.container()

        baseline_revenue = st.session_state.sim[0]
        sim_revenue = st.session_state.sim[1]
        baseline_qty = st.session_state.sim[2]
        new_qty = st.session_state.sim[3]
        investment = st.session_state.sim[4]
        new_price = st.session_state.sim[5]

        with panel1:
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Baseline Revenue", value=f"${round(baseline_revenue)}")
            col2.metric(label="Simulated Revenue", value=f"${round(sim_revenue)}")
            col3.metric(label="Revenue Change", value=f"${round(sim_revenue) - round(baseline_revenue)}", delta=f"{round(((sim_revenue/baseline_revenue)-1)*100,1)}%")
        
        with panel2:
            col1, col2, col3 = st.columns(3)
            col1.metric(label="Baseline Qty", value=f"{round(baseline_qty)}")
            col2.metric(label="Simulated Qty", value=f"{round(new_qty)}")
            col3.metric(label="% Qty Change", value = f"{round(new_qty) - round(baseline_qty)}", delta=f"{round(((new_qty/baseline_qty)-1)*100,1)}%")
    
        st.subheader(f"Investment Needed for {st.session_state.user_p}% Price Reduction: ${round(investment)}")
        
        st.markdown("#### Item Price Change")

        chart_data_2 = pd.DataFrame({'Item':st.session_state.elastic['ITEM'], 'Base Price':np.around(bp,2),'New Price':np.around(new_price,2)})
        chart2 = alt.Chart(chart_data_2.melt('Item')).mark_bar().encode(
                alt.Y('variable:N', axis=alt.Axis(title='')),
                alt.X('value:Q', axis=alt.Axis(title='price', grid=False, format='$.2f')),
                color=alt.Color('variable:N'),
                row=alt.Row('Item:O', header = alt.Header(labelAngle=0, labelAlign='left'))).configure_view(stroke='transparent')
        st.altair_chart(chart2, theme="streamlit", use_container_width=True)
        st.download_button(label="Download",data=chart_data_2.to_csv(index=False).encode('utf-8'),file_name='scenario_price_change.csv',mime='text/csv',)
    
else:
    st.title(":orange[Finish Previous Tabs!]")

