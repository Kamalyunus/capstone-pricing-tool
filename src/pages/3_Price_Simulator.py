import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

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


if st.session_state.key is not '':

    st.title("Simulation Results")

    df = st.session_state['key']

    e = df.elasticities.to_numpy()
    bp = df.current_price.to_numpy()
    bq = df.base_qty.to_numpy()
    num_items = e.size 

    max_price = st.sidebar.slider("Price Reduction for All Items:",0,50,10, step=5, help = "Price Reduction per Item ", format="%d%%")
    user_price = np.ones(num_items)*(max_price/100)

    if st.sidebar.button("Calculate"):
        with st.spinner("Please Wait..."):

            baseline_revenue, sim_revenue, baseline_qty, new_qty, investment, new_price = simulate(-user_price,e,bp,bq) 
            panel1=st.container()
            panel2=st.container()
            

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
        
            st.subheader(f"Investment Needed for {max_price}% Price Reduction: ${round(investment)}")
            
            st.subheader("Item Price Change")

            chart_data_2 = pd.DataFrame({'Item':df.item, 'Base Price':np.around(bp,2),'New Price':np.around(new_price,2)})
            chart2 = alt.Chart(chart_data_2.melt('Item')).mark_bar().encode(
                    alt.Y('variable:N', axis=alt.Axis(title='')),
                    alt.X('value:Q', axis=alt.Axis(title='price', grid=False, format='$.2f')),
                    color=alt.Color('variable:N'),
                    row='Item:O').configure_view(stroke='transparent')
            st.altair_chart(chart2, theme="streamlit", use_container_width=True)
    
else:
    st.title(":orange[Upload a File under Home Tab!]")

