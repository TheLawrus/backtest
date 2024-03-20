import pandas as pd
import matplotlib.pyplot as plt


rsi_df = pd.read_csv('RSI.csv') # load the factors from .csv file

ret_list = [] # everyday's return based on our factor
for i in range(14, 100):#1300 # iterate through every day in backtesting window
    ret = 0 # initialize return of that day to 0
    date = rsi_df['Date'][i]
    tomorrow_date = rsi_df['Date'][i+1]

    sorted_RSI = rsi_df.iloc[i][1:].sort_values().dropna()[:10].index # rank the tickers with factor value
                                                                      #drop the NAN ones, take the first 10 tickers with highest factor value
    for symbol in sorted_RSI:
        # load the close price for these 10 tickers we want to trade at the end of that day
        df = pd.read_csv(f"C:/Users/Arjun/Documents/GitHub/EDA/CardinalTradingSystem/Data/{symbol}.csv", index_col=0, parse_dates=True) 
        today_close = df['Close'][date]
        tomorrow_close = df['Close'][tomorrow_date]
        # calculate the return for each ticker, sum it up
        ret += (tomorrow_close - today_close) / today_close 
        
    ret_list.append(ret/10) # divide it by 10 because we have to spilt our position evenly
    #print(i) # logging

# calculate the cummulative return so that we can plot
cumulative_sum = [ret_list[0]]
for num in ret_list[1:]:
    cumulative_sum.append(cumulative_sum[-1] + num)

plt.plot(cumulative_sum)
plt.show()
