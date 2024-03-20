import pandas as pd
import matplotlib.pyplot as plt


sentiment_df = pd.read_csv('sentiment_recent.csv') # load the factors from .csv file

sentiment_list = [] # everyday's return based on our factor
SP500_list = [] # everyday's return for SP500 for comparison
SP500_df = pd.read_csv('RecentData\^GSPC.csv', parse_dates=True)

date_list = SP500_df['Date']
ret_list = []

NUM_POOL = 2

for i in range(len(date_list) - 1):
    ret = 0 # initialize return of that day to 0
    date = SP500_df['Date'][i]
    tomorrow_date = SP500_df['Date'][i+1]

    SP500_list.append((SP500_df['Close'][i+1] - SP500_df['Close'][i]) / SP500_df['Close'][i]) # calculate SP500's return

    current_sentiment = sentiment_df.iloc[i][1:]
    sorted_sentiment = current_sentiment.sort_values(ascending=False)
    sorted_sentiment = sorted_sentiment.dropna()
    # print(sorted_sentiment)
    # print(sorted_sentiment)
    # rank the tickers with factor value
    # drop the NAN ones, take the first 100 tickers with highest factor value
    selected_tickers = []
    for symbol in sorted_sentiment.index:
        
        score = float(sorted_sentiment[symbol].strip('()').split(',')[0])
        count = int(sorted_sentiment[symbol].strip('()').split(',')[1])
        if count >= 7 and score >= 0.70:
            if len(selected_tickers) == NUM_POOL:
                break
            selected_tickers.append(symbol)
            try:
                df = pd.read_csv(f"RecentData/{symbol}.csv", index_col=0, parse_dates=True) 
            except:
                continue
            today_close = df['Close'][date]
            tomorrow_close = df['Close'][tomorrow_date]
            ret += (tomorrow_close - today_close) / today_close 
    ret_list.append(ret/NUM_POOL)

    print(date_list[i]) # logging
    print(selected_tickers)
    print(ret/NUM_POOL)

cumulative_sum = [ret_list[0]]
for num in ret_list[1:]:
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
