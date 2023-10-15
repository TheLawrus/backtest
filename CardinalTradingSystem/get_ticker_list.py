import pandas as pd

# Retrieve the list of S&P 500 companies from Wikipedia
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
sp500_table = pd.read_html(url)[0]

# Extract the ticker symbols from the table
tickers = sp500_table['Symbol'].tolist()

# Write the ticker symbols to a CSV file
with open('sp500_tickers.csv', 'w') as f:
    for ticker in tickers:
        f.write(f"{ticker}\n")