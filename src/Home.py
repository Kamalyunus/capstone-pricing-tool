import pandas as pd
import streamlit as st
import numpy as np

option = st.sidebar.radio("Pick Option", ('Upload File', 'Simulate Data'))

@st.experimental_memo
def get_data(file):
    df = pd.read_csv(file)
    return df

@st.experimental_memo
def simulate_data(n):
    bq = pd.Series(np.random.randint(50, 500, size=n)) # Item Baseline Forecast
    bp = pd.Series(np.random.randint(5, 10, size=n) + np.random.rand(n))  # Item Current Prices
    e = pd.Series(3 * np.random.rand(n) - 3) # Price Elasticities
    item = pd.Series(np.arange(n) + 1, dtype = str)
    df_series = {'item':item, 'current_price':bp, "base_qty":bq, 'elasticities':e}
    df = pd.DataFrame(df_series)
    return df
    

if option == "Upload File":
    uploaded_file = st.sidebar.file_uploader("Upload file", type = ['csv'])

    if uploaded_file is not None:
        df = get_data(uploaded_file)
        st.session_state["key"] = df

    if 'key' not in st.session_state:
        st.session_state['key'] = ''

    st.write(st.session_state["key"])

else:
    item_count = st.sidebar.number_input('Enter Item Count', 2, 100,value=10)
    
    if st.sidebar.button('Simulate'):    
        df = simulate_data(item_count)
        st.session_state["key"] = df

        if 'key' not in st.session_state:
            st.session_state['key'] = ''

        st.write(st.session_state["key"])