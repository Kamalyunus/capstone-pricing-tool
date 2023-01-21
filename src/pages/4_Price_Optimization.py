import streamlit as st
import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution, NonlinearConstraint, Bounds
import altair as alt

def objective_func(x, e, bp, bq):
    perc_qty_change = np.multiply(e,x)
    new_price = bp + np.multiply(bp,x)
    new_qty = bq + np.multiply(perc_qty_change,bq)
    revenue = np.dot(new_price, new_qty)
    return -revenue

def investment(x,bp,bq):
    new_price = bp + np.multiply(bp,x)
    lm = bp - new_price
    investment = np.dot(lm,bq)
    return investment

if st.session_state.key is not '':

    st.title("Optimization Results")

    df = st.session_state['key']

    e = df.elasticities.to_numpy()
    bp = df.current_price.to_numpy()
    bq = df.base_qty.to_numpy()

    budget = np.dot(bp,bq)

    max_budget=st.sidebar.slider("Budget:",0,round(int(budget),-3),round(int(0.3*budget),-2), step=50, help = "Max Budget Available for Price Investment",format="$%d")

    max_price=st.sidebar.slider("Maximum Price Reduction:",0,50,10, step=5, help = "Maximum Price Reduction Allowed per Item ", format="%d%%")

    num_items = e.size # number of items

    if st.sidebar.button("Optimize"):
        with st.spinner("Please Wait..."):

            #Solver
            best = differential_evolution(
                    objective_func,
                    x0 = -(max_price/100)*np.ones(num_items)*0.5,
                    args=(e,bp,bq),
                    bounds=Bounds(lb=-(max_price/100)*np.ones(num_items), ub=np.zeros(num_items)),
                    constraints=NonlinearConstraint(lambda x: investment(x,bp,bq), lb = 0, ub = max_budget),
                    seed = 1234
            )

            # Print Results
            if best.success:
                new_price = bp + np.multiply(bp,best.x)
                perc_qty_change = np.multiply(e,best.x)
                new_qty = bq + np.multiply(perc_qty_change,bq)
                baseline_revenue = np.dot(bp,bq)
                baseline_qty=sum(bq)

                st.header(":green[Optimal Solution Found]")

                panel1=st.container()
                panel2=st.container()

                with panel1:
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="Baseline Revenue", value=f"${round(baseline_revenue)}")
                    col2.metric(label="Optimize Revenue", value=f"${-round(best.fun)}")
                    col3.metric(label="Revenue Change", value=f"${-round(best.fun) - round(baseline_revenue)}", delta=f"{round(((-best.fun/baseline_revenue)-1)*100,1)}%")
                
                with panel2:
                    col1, col2, col3 = st.columns(3)
                    col1.metric(label="Baseline Qty", value=f"{round(baseline_qty)}")
                    col2.metric(label="Optimize Qty", value=f"{round(sum(new_qty))}")
                    col3.metric(label="% Qty Change", value = f"{round(sum(new_qty)) - round(baseline_qty)}", delta=f"{round(((sum(new_qty)/baseline_qty)-1)*100,1)}%")

                st.subheader(f"Budget Used: ${round(investment(best.x,bp,bq))}")

                tab1, tab2 = st.tabs(["Item Price Change", "Optimal Item Price"])

                with tab2:
                    chart_data_1 = pd.DataFrame({'% Price Change':np.around(best.x,3),'Item':df.item})
                    chart1 = alt.Chart(chart_data_1).mark_bar().encode( x=alt.X('% Price Change', axis = alt.Axis(format='%')), y='Item')
                    st.altair_chart(chart1, theme="streamlit", use_container_width=True)

                with tab1:
                    chart_data_2 = pd.DataFrame({'Item':df.item, 'Base Price':np.around(bp,2),'New Price':np.around(new_price,2)})
                    chart2 = alt.Chart(chart_data_2.melt('Item')).mark_bar().encode(
                            alt.Y('variable:N', axis=alt.Axis(title='')),
                            alt.X('value:Q', axis=alt.Axis(title='price', grid=False, format='$.2f')),
                            color=alt.Color('variable:N'),
                            row='Item:O').configure_view(stroke='transparent')
                    st.altair_chart(chart2, theme="streamlit", use_container_width=True)
                
            else: 
                st.header(":red[No solution found to problem]")

else:
    st.title(":orange[Upload a File under Home Tab!]")

