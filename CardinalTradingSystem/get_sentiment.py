import pandas as pd
import requests
import time

# Constants
API_TOKEN = '65356c15cdf9d7.54924335'
API_URL = 'https://eodhd.com/api/sentiments'
FROM_DATE = '2019-01-03'
TO_DATE = '2023-03-03'

# Load tickers
tickers_df = pd.read_csv('sp500_tickers.csv', header=None)
all_tickers = tickers_df[0].tolist()
all_tickers = [ticker.lower() for ticker in all_tickers]

# Initialize the final DataFrame with Date as the index
final_df = pd.DataFrame()
A_df = pd.read_csv('Data/A.csv')
final_df['Date'] = A_df['Date']
final_df.set_index('Date', inplace=True)

# Split tickers into chunks of 100
ticker_chunks = [all_tickers[i:i + 100] for i in range(0, len(all_tickers), 100)]
# ticker_chunks = [all_tickers[i:i + 10] for i in range(0, 50, 10)]


sentiments_dict = {}

def change_ticker(ticker):
    return ticker.split('.')[0]

for chunk in ticker_chunks:
    tickers_str = ','.join(chunk)
    payload = {
        's': tickers_str,
        'from': FROM_DATE,
        'to': TO_DATE,
        'api_token': API_TOKEN
    }

    response = requests.get(API_URL, params=payload)
    data = response.json()

    # Debug: print the data to see if the responses contain non-zero sentiments
    # print(data)
    print(chunk)

    # Process the response data
    for ticker, sentiments in data.items():
        ticker_dates = []  # Dates specific to this ticker
        sentiments_list = []  # Sentiments for the dates

        for sentiment in sentiments:
            date = sentiment['date']
            if date not in final_df.index:
                continue
            value = sentiment['normalized']  # or any other value you're interested in
            count = sentiment['count']

            ticker_dates.append(date)  # Add date specific to this ticker
            sentiments_list.append((value, count))  # Corresponding sentiment value

        if sentiments_list:
            # Ensure we are using the correct dates for this ticker's data
            sentiments_dict[change_ticker(ticker)] = pd.Series(sentiments_list, index=ticker_dates)

    # Pause to avoid hitting rate limit
    # time.sleep(2)

# Construct DataFrame from the dictionary
if sentiments_dict:
    final_df = pd.DataFrame(sentiments_dict)
    # Save the CSV
    final_df.to_csv('sentiment.csv', index_label='Date')
