# MSDS 498: Price Optimization Tool

## App is designed to provide optimal pricing strategy for a given budget

## Getting Started:
Upload file having weekly time series data containing item sold quantity and selling price. Any relevant feature can also be included to improve price elasticities and demand forecast prediction

The CSV file must have following columns (ITEM - DATE are composite primary key columns):
- *ITEM*: Item description (string) 
- *DATE*: Week start/end date (MM/DD/YYYY) 
- *UNITS*: Item volume for the week (float) 
- *PRICE*: Selling price of the item (float)

## App Tab Details:
- **Demand Forecast Tab**: Uses uploaded weekly historical sales data to create a 4 weeks of demand forecast, taking into account factors such as seasonality and trends
- **Price Elasticities Tab**: Estimates how changes in price will affect demand for a given item
- **Price Simulator Tab**: Simulate 'What-If' price change scenarios impact on demand and budget requirement
- **Price Optimization Tab**: Leverage Demand Forecast, Available Budget and Price Elasticities to recommend optimal prices to maximize revenue

## Local Installation:
 Run following commands[^1]:

 ```
 git clone https://github.com/Kamalyunus/capstone-pricing-tool.git
 cd capstone-pricing-tool
 docker build -t capstonepricingtool:latest . 
 docker run -p 8501:8501 -d capstonepricingtool:latest
 ```
 Access app at  http://localhost:8501/ in your browser

## Cloud Deployment:

Fork the Github repo above and follow instruction provided at this link:  
https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app 

Sample Data is present in folder to get started

 [^1]: Note Docker and Git installation are Prerequisite