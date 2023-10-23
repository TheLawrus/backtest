import pandas as pd
import matplotlib.pyplot as plt


sentiment_df = pd.read_csv('sentiment.csv') # load the factors from .csv file

sentiment_list = [] # everyday's return based on our factor
SP500_list = [] # everyday's return for SP500 for comparison
SP500_df = pd.read_csv('Data\^GSPC.csv', index_col=0, parse_dates=True)

for i in range(0,len(sentiment_df) - 1):#1300 # iterate through every day in backtesting window
    ret = 0 # initialize return of that day to 0
    date = sentiment_df['Date'][i]
    tomorrow_date = sentiment_df['Date'][i+1]

    SP500_list.append((SP500_df['Close'][tomorrow_date] - SP500_df['Close'][date]) / SP500_df['Close'][date]) # calculate SP500's return

    current_sentiment = sentiment_df.iloc[i][1:]
    sorted_sentiment = current_sentiment.sort_values(ascending=False)
    sorted_sentiment = sorted_sentiment.dropna()[:20].index
    # print(sorted_sentiment)
    # rank the tickers with factor value
    # drop the NAN ones, take the first 10 tickers with highest factor value
    count = 0 # count the valid stock we can buy today
    for symbol in sorted_sentiment:
        # load the close price for these 10 tickers we want to trade at the end of that day
        df = pd.read_csv(f"Data/{symbol}.csv", index_col=0, parse_dates=True) 
        if len(df['Close']) == 0:
            continue
        count += 1
        today_close = df['Close'][date]
        tomorrow_close = df['Close'][tomorrow_date]
        # calculate the return for each ticker, sum it up
        ret += (tomorrow_close - today_close) / today_close 
        
    sentiment_list.append(ret/count) # divide it by count because we have to spilt our position evenly
    print(i) # logging

# calculate the cummulative return so that we can plot
cumulative_sum = [sentiment_list[0]]
for num in sentiment_list[1:]:
    cumulative_sum.append(cumulative_sum[-1] + num)

SP500_sum = [SP500_list[0]]
for num in SP500_list[1:]:
    SP500_sum.append(SP500_sum[-1] + num)

excess_return = [cumulative_sum[i] - SP500_sum[i] for i in range(len(cumulative_sum))]

plt.plot(cumulative_sum)
plt.plot(SP500_sum)
plt.plot(excess_return)
plt.legend(["Strategy", "SP500", "Excess Return"], loc ="lower right") 
plt.show()

