import pandas as pd
import streamlit as st
import numpy as np

# option = st.sidebar.radio("Pick Option", ('Upload File', 'Simulate Data'))

@st.experimental_memo
def get_data(file):
    df = pd.read_csv(file)
    return df
    

st.set_page_config(
    page_title="Price Optimization App",
    menu_items={
        'About': "# MSDS 498 CAPSTONE PROJECT: Pricing Optimization "
    }
)

st.title("Price Optimization App")
st.caption("App is designed to provide optimal pricing strategy for a given budget" )
st.markdown("### Getting Started:")
st.markdown(":orange[Upload file having weekly time series data containing item sold quantity and selling price. Any relevant feature can also be included to improve price elasticities and demand forecast prediction]")
st.warning("The CSV file must have ITEM, DATE, UNITS, PRICE as column names")
st.markdown("* ***Demand Forecast Tab***: Uses uploaded weekly historical sales data to create a 4 weeks of demand forecast, taking into account factors such as seasonality and trends")
st.markdown("* ***Price Elasticities Tab***: Estimates how changes in price will affect demand for a given item")
st.markdown("* ***Price Simulator Tab***: Simulate 'What-If' price change scenarios impact on demand and budget requirement")
st.markdown("* ***Price Optimization Tab***: Leverage Demand Forecast, Available Budget and Price Elasticities to recommend optimal prices to maximize revenue ")

def callback_upl():
    st.session_state['upl'] = True

if 'df' not in st.session_state:
    st.session_state['df'] = ''

if 'upl' not in st.session_state:
    st.session_state['upl'] = False

uploaded_file = st.sidebar.file_uploader("Upload file", type = ['csv'], on_change=callback_upl)
if uploaded_file is not None:
    df = get_data(uploaded_file)
    st.session_state["df"] = df

if st.session_state.upl:
    st.markdown("Sample of Uploaded Data:")
    st.dataframe(st.session_state.df.head(), use_container_width = True)
    st.write(f"Number of Unique Items: {st.session_state.df.ITEM.nunique()}")




    

