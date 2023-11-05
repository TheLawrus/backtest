import pandas as pd
import ta

# Read the ticker symbols from the CSV file
tickers_df = pd.read_csv('sp500_tickers.csv', header=None)

# Convert the DataFrame to a list
tickers = tickers_df[0].tolist()

# Create empty DataFrames to store the MACD, Signal Line, and Histogram values
macd_df = pd.DataFrame()
signal_df = pd.DataFrame()
histogram_df = pd.DataFrame()

count = 0

# Loop through the tickers and read the stock market data from CSV files
for symbol in tickers:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(f"C:/Users/Arjun/Documents/GitHub/EDA/CardinalTradingSystem/Data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calculate the MACD using the ta library
    macd = ta.trend.MACD(df['Close'])
    
    # Add the MACD, Signal Line, and Histogram values to their respective DataFrames
    macd_df[symbol] = macd.macd()
    signal_df[symbol] = macd.macd_signal()
    histogram_df[symbol] = macd.macd_diff()

    count += 1
    #print(count)

# Write the DataFrames to CSV files
macd_df.to_csv("MACD.csv")
signal_df.to_csv("Signal.csv")
histogram_df.to_csv("Histogram.csv")
