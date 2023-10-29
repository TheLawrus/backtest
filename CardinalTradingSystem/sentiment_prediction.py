import pandas as pd
import matplotlib.pyplot as plt


sentiment_df = pd.read_csv('sentiment_recent.csv') # load the factors from .csv file

sentiment_list = [] # everyday's return based on our factor
SP500_list = [] # everyday's return for SP500 for comparison
SP500_df = pd.read_csv('Data\^GSPC.csv', index_col=0, parse_dates=True)

date_list = sentiment_df['Date']

for i in range(len(date_list)):
    ret = 0 # initialize return of that day to 0
    # date = sentiment_df['Date'][i]
    # tomorrow_date = sentiment_df['Date'][i+1]

    # SP500_list.append((SP500_df['Close'][tomorrow_date] - SP500_df['Close'][date]) / SP500_df['Close'][date]) # calculate SP500's return

    current_sentiment = sentiment_df.iloc[i][1:]
    sorted_sentiment = current_sentiment.sort_values(ascending=False)
    sorted_sentiment = sorted_sentiment.dropna()[:200]
    # print(sorted_sentiment)
    # print(sorted_sentiment)
    # rank the tickers with factor value
    # drop the NAN ones, take the first 100 tickers with highest factor value
    selected_tickers = []
    for symbol in sorted_sentiment.index:
        
        count = int(sorted_sentiment[symbol].strip('()').split(',')[1])
        if count >= 3:
            if len(selected_tickers) == 3:
                break
            selected_tickers.append(symbol)

    print(date_list[i]) # logging
    print(selected_tickers)

