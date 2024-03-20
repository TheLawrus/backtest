import pandas as pd
import ta

# Read the ticker symbols from the CSV file
tickers_df = pd.read_csv('sp500_tickers.csv', header=None)

# Convert the DataFrame to a list
tickers = tickers_df[0].tolist()
# print(tickers)

# Create an empty DataFrame to store the RSI values
rsi_df = pd.DataFrame()

count = 0

# Loop through the tickers and read the stock market data from CSV files
for symbol in tickers:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(f"C:/Users/15104/Documents/Cardinal/CardinalTradingSystem/Data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calculate the RSI using the ta library
    rsi = ta.momentum.RSIIndicator(df['Close']).rsi()

    # Add the RSI values to the DataFrame
    rsi_df[symbol] = rsi
    count += 1
    print(count)

# Write the DataFrame to a CSV file
rsi_df.to_csv("RSI.csv")
