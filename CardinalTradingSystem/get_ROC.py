import pandas as pd
import ta

# Read the ticker symbols from the CSV file
tickers_df = pd.read_csv('sp500_tickers.csv', header=None)

# Convert the DataFrame to a list
tickers = tickers_df[0].tolist()

# Create an empty DataFrame to store the ROC values
roc_df = pd.DataFrame()

count = 0

# Loop through the tickers and read the stock market data from CSV files
for symbol in tickers:
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_csv(f"C:/Users/Arjun/Documents/GitHub/EDA/CardinalTradingSystem/Data/{symbol}.csv", index_col=0, parse_dates=True)

    # Calculate the ROC using the ta library
    roc = ta.momentum.ROCIndicator(df['Close']).roc()

    # Add the ROC values to the DataFrame
    roc_df[symbol] = roc
    count += 1
    #print(count)

# Write the DataFrame to a CSV file
roc_df.to_csv("ROC.csv")