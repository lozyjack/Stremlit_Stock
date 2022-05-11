import requests
import json
import pandas as pd
import streamlit as st
import yfinance as yf
from scrape_stock import symbol_list_id
import streamlit.components.v1 as components
import datetime as dt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import date
import numpy as np



st.set_page_config(
    page_title="StockPeex",
    layout="wide")

#Input Box For Search Type
CHOICES = {"symbol": "Ticker", "company_name":"Company Name" }

#Extracting Ticker Data
ticker_list_raw = [[d['symbol'] for d in symbol_list_id if 'symbol' in d]]
ticker_list = ticker_list_raw[0]
ticker_list_display = [x[:-3] for x in ticker_list]
ticker_zip = zip(ticker_list, ticker_list_display)
ticker_dict = dict(ticker_zip)

#Extracting Company Name Data
companyName_list_raw = [[d['longName'] for d in symbol_list_id if 'longName' in d]]
companyName_list = companyName_list_raw[0]
companyName_zip = zip(ticker_list, companyName_list)
companyName_dict = dict(companyName_zip)

ticker = ""

#Sidebar
with st.sidebar:
    
    def format_func(option):
        return CHOICES[option]
    option = st.selectbox("Search By", options=list(CHOICES.keys()), format_func=format_func)
    #st.write(f"You selected option {option} called {format_func(option)}")

    if option is "symbol":
        def format_func_ticker(ticker_seleceted):
            return ticker_dict[ticker_seleceted]
        ticker_selectbox = st.selectbox("Search By", options=list(ticker_dict.keys()), format_func=format_func_ticker)
        st.write(f"You selected option {ticker_selectbox} called {format_func_ticker(ticker_selectbox)}") 
        ticker = ticker_selectbox
    else:
        def format_func_companyName(ticker_seleceted):
            return companyName_dict[ticker_seleceted]
        companyName_selectbox = st.selectbox("Search By", options=list(companyName_dict.keys()), format_func=format_func_companyName)
        st.write(f"You selected option {companyName_selectbox} called {format_func_companyName(companyName_selectbox)}") 
        ticker = companyName_selectbox
        

#CHARTING

a_chartin, b_chartin, c_chartin = st.columns(3)

input_interval = a_chartin.selectbox(
        "Select Inteval:",
        ("1d", "5d", "1wk", "1mo", "3mo")
    )
date_from = b_chartin.date_input(
     "from",
     dt.date(2019, 7, 6))

date_to = c_chartin.date_input(
     "to",
     dt.date(2022,1,1))


stock = yf.Ticker(ticker)
history_data = stock.history(interval = input_interval, start = date_from, end = date_to)

prices = history_data['Close']
volumes = history_data['Volume']

lower = prices.min()
upper = prices.max()
prices_ax = np.linspace(lower,upper, num=20)

vol_ax = np.zeros(20)

for i in range(0, len(volumes)):
    if(prices[i] >= prices_ax[0] and prices[i] < prices_ax[1]):
        vol_ax[0] += volumes[i]   
        
    elif(prices[i] >= prices_ax[1] and prices[i] < prices_ax[2]):
        vol_ax[1] += volumes[i]  
        
    elif(prices[i] >= prices_ax[2] and prices[i] < prices_ax[3]):
        vol_ax[2] += volumes[i] 
        
    elif(prices[i] >= prices_ax[3] and prices[i] < prices_ax[4]):
        vol_ax[3] += volumes[i]  
        
    elif(prices[i] >= prices_ax[4] and prices[i] < prices_ax[5]):
        vol_ax[4] += volumes[i]  
        
    elif(prices[i] >= prices_ax[5] and prices[i] < prices_ax[6]):
        vol_ax[5] += volumes[i] 
        
    elif(prices[i] >= prices_ax[6] and prices[i] < prices_ax[7]):
        vol_ax[6] += volumes[i] 

    elif(prices[i] >= prices_ax[7] and prices[i] < prices_ax[8]):
        vol_ax[7] += volumes[i] 

    elif(prices[i] >= prices_ax[8] and prices[i] < prices_ax[9]):
        vol_ax[8] += volumes[i] 

    elif(prices[i] >= prices_ax[9] and prices[i] < prices_ax[10]):
        vol_ax[9] += volumes[i] 

    elif(prices[i] >= prices_ax[10] and prices[i] < prices_ax[11]):
        vol_ax[10] += volumes[i] 

    elif(prices[i] >= prices_ax[11] and prices[i] < prices_ax[12]):
        vol_ax[11] += volumes[i] 

    elif(prices[i] >= prices_ax[12] and prices[i] < prices_ax[13]):
        vol_ax[12] += volumes[i] 

    elif(prices[i] >= prices_ax[13] and prices[i] < prices_ax[14]):
        vol_ax[13] += volumes[i] 

    elif(prices[i] >= prices_ax[14] and prices[i] < prices_ax[15]):
        vol_ax[14] += volumes[i]   
        
    elif(prices[i] >= prices_ax[15] and prices[i] < prices_ax[16]):
        vol_ax[15] += volumes[i] 
        
    elif(prices[i] >= prices_ax[16] and prices[i] < prices_ax[17]):
        vol_ax[16] += volumes[i]         
        
    elif(prices[i] >= prices_ax[17] and prices[i] < prices_ax[18]):
        vol_ax[17] += volumes[i]         
        
    elif(prices[i] >= prices_ax[18] and prices[i] < prices_ax[19]):
        vol_ax[18] += volumes[i] 
    
    else:
        vol_ax[19] += volumes[i]

fig = make_subplots(
        rows=1, cols=2,
        column_widths=[0.2, 0.8],
        specs=[[{}, {}]],
        horizontal_spacing = 0.01
    )

fig.add_trace(
        go.Bar(
                x = vol_ax, 
                y= prices_ax,
                text = np.around(prices_ax,2),
                textposition='auto',
                orientation = 'h'
            ),
        row = 1, col =1
    )

dateStr = history_data.index.strftime("%d-%m-%Y")

fig.add_trace(
    go.Candlestick(x=dateStr,
                open=history_data['Open'],
                high=history_data['High'],
                low=history_data['Low'],
                close=history_data['Close'],
                yaxis= "y2"  
            ),
        row = 1, col=2
    )
        
fig.update_layout(
    title_text='Market Profile Chart', # title of plot
    bargap=0.01, # gap between bars of adjacent location coordinates,
    showlegend=False,
    
    xaxis = dict(
            showticklabels = False
        ),
    yaxis = dict(
            showticklabels = False
        ),
    
    yaxis2 = dict(
            title = "Price (IDR)",
            side="right"
        )
)

fig.update_yaxes(nticks=20)
fig.update_yaxes(side="right")
fig.update_layout(height=800)

config={
        'modeBarButtonsToAdd': ['drawline']
    }

st.plotly_chart(fig, use_container_width=True, config=config)





url = 'https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+ ticker +'?modules=incomeStatementHistory'
r = requests.get(url = url, headers = {'User-agent': 'Mozilla/5.0'})

data = r.json()
s = data['quoteSummary']['result'][0]['incomeStatementHistory']['incomeStatementHistory']
df = pd.json_normalize(s)
new_df_list = ['endDate.fmt','totalRevenue.raw','costOfRevenue.raw','grossProfit.raw','researchDevelopment.raw','sellingGeneralAdministrative.raw','totalOperatingExpenses.raw','operatingIncome.raw','totalOtherIncomeExpenseNet.raw','ebit.raw','incomeBeforeTax.raw','incomeTaxExpense.raw','netIncomeFromContinuingOps.raw','netIncome.raw','netIncomeApplicableToCommonShares.raw',
]
newDF = df[df.columns.intersection(new_df_list)]

final = newDF.rename(columns={'endDate.fmt':'Date','totalRevenue.raw':'Total Revenue',
'costOfRevenue.raw':'Cost Revenue',
'grossProfit.raw':'Gross Profit',
'researchDevelopment.raw':'Research and Development',
'sellingGeneralAdministrative.raw':'Selling General Administrative',
'totalOperatingExpenses.raw':'Total Operating Expenses',
'operatingIncome.raw':'Operating Income',
'totalOtherIncomeExpenseNet.raw':'Total Other Income (Expense)',
'ebit.raw':'EBIT',
'incomeBeforeTax.raw':'Income Tax',
'incomeTaxExpense.raw':'Income Expense',
'netIncomeFromContinuingOps.raw':'Net Income From Continuein Opearations',
'netIncome.raw':'Net Income',
'netIncomeApplicableToCommonShares.raw':'Net income Applicable To Common Shares'
}
)

Income_Statement = final.set_index("Date").transpose()
st.write(Income_Statement)

st.write(ticker)