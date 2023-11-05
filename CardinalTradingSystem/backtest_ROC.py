import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the ROC and RSI values from the CSV file
roc_df = pd.read_csv('ROC.csv')
rsi_df = pd.read_csv('RSI.csv')

roc_ret_list = []  # Return list for ROC strategy
rsi_ret_list = []  # Return list for RSI strategy
sp500_ret_list = []  # Return list for S&P 500

# Define the data folder
data_folder = "C:/Users/Arjun/Documents/GitHub/EDA/CardinalTradingSystem/Data/"

# iterate through every day in backtesting window
for i in range(14, 100):  # Adjust this range as per your data size
    roc_ret = 0  # Initialize return of that day to 0 for ROC
    rsi_ret = 0  # Initialize return of that day to 0 for RSI
    sp500_daily_return = 0  # Initialize return of that day to 0 for S&P 500

    date = roc_df['Date'][i]
    tomorrow_date = roc_df['Date'][i+1]

    # Rank the tickers with ROC values: take the first 10 tickers with highest momentum
    sorted_ROC = roc_df.iloc[i][1:].sort_values(ascending=False).dropna()[:10].index
    sorted_RSI = rsi_df.iloc[i][1:].sort_values().dropna()[:10].index

    for symbol in sorted_ROC:
        # Load the close price for these 10 tickers we want to trade at the end of that day
        df = pd.read_csv(os.path.join(data_folder, f"{symbol}.csv"), index_col=0, parse_dates=True)
        today_close = df['Close'][date]
        tomorrow_close = df['Close'][tomorrow_date]
        
        # Calculate the return for each ticker, sum it up for ROC
        roc_ret += (tomorrow_close - today_close) / today_close

    for symbol in sorted_RSI:
        # Load the close price for these 10 tickers we want to trade at the end of that day
        df = pd.read_csv(os.path.join(data_folder, f"{symbol}.csv"), index_col=0, parse_dates=True)
        today_close = df['Close'][date]
        tomorrow_close = df['Close'][tomorrow_date]
        
        # Calculate the return for each ticker, sum it up for RSI
        rsi_ret += (tomorrow_close - today_close) / today_close

    # Compute average daily return for S&P 500
    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_folder, filename), index_col=0, parse_dates=True)
            if date in df.index and tomorrow_date in df.index:
                today_close = df['Close'][date]
                tomorrow_close = df['Close'][tomorrow_date]
                sp500_daily_return += (tomorrow_close - today_close) / today_close

    sp500_daily_return /= len(os.listdir(data_folder))  # Average it out
    sp500_ret_list.append(sp500_daily_return)

    # Divide returns by 10 as we split our position evenly
    roc_ret_list.append(roc_ret/10)
    rsi_ret_list.append(rsi_ret/10)

# Calculate the cumulative return for both strategies and S&P 500
cumulative_roc = [roc_ret_list[0]]
for num in roc_ret_list[1:]:
    cumulative_roc.append(cumulative_roc[-1] + num)

cumulative_rsi = [rsi_ret_list[0]]
for num in rsi_ret_list[1:]:
    cumulative_rsi.append(cumulative_rsi[-1] + num)

cumulative_sp500 = [sp500_ret_list[0]]
for num in sp500_ret_list[1:]:
    cumulative_sp500.append(cumulative_sp500[-1] + num)

# Plotting
plt.plot(cumulative_roc, label="ROC Strategy", color="blue")
plt.plot(cumulative_rsi, label="RSI Strategy", color="green")
plt.plot(cumulative_sp500, label="S&P 500", color="red")
plt.title("Performance Comparison: ROC vs RSI vs S&P 500")
plt.xlabel("Days")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.show()
