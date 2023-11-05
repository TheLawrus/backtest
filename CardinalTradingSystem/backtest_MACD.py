import pandas as pd
import matplotlib.pyplot as plt
import os

# Load the ROC, RSI, and MACD values from the CSV files
roc_df = pd.read_csv('ROC.csv')
rsi_df = pd.read_csv('RSI.csv')
macd_df = pd.read_csv('MACD.csv')
signal_df = pd.read_csv('Signal.csv')

roc_ret_list = []  # Return list for ROC strategy
rsi_ret_list = []  # Return list for RSI strategy
macd_ret_list = []  # Return list for MACD strategy
sp500_ret_list = []  # Return list for S&P 500
macd_excess_ret_list = []

# Define the data folder
data_folder = "C:/Users/Arjun/Documents/GitHub/EDA/CardinalTradingSystem/Data/"


# Iterate through every day in backtesting window
for i in range(14, 800):  # Adjust this range as per your data size
    roc_ret = 0
    rsi_ret = 0
    macd_ret = 0
    sp500_daily_return = 0

    date = roc_df['Date'][i]
    tomorrow_date = roc_df['Date'][i+1]

    sorted_ROC = roc_df.iloc[i][1:].sort_values(ascending=False).dropna()[:10].index
    sorted_RSI = rsi_df.iloc[i][1:].sort_values().dropna()[:10].index
    
    # MACD strategy: Buy when MACD > Signal line
    macd_above_signal = (macd_df.iloc[i][1:] > signal_df.iloc[i][1:]).dropna()
    sorted_MACD = macd_above_signal[macd_above_signal].index[:10]
    
    
    
    
    for symbol in sorted_ROC:
        try:
            # Load the close price for these 10 tickers we want to trade at the end of that day
            df = pd.read_csv(os.path.join(data_folder, f"{symbol}.csv"), index_col=0, parse_dates=True)
            today_close = df.loc[date, 'Close']
            tomorrow_close = df.loc[tomorrow_date, 'Close']
            
            # Calculate the return for each ticker, sum it up for ROC
            roc_ret += (tomorrow_close - today_close) / today_close
        except FileNotFoundError:
            print(f"File for {symbol} not found. Skipping...")
            continue 
        except KeyError as e:
            print(f"Key error {e} - possible missing date in {symbol}.csv")
            continue

    for symbol in sorted_RSI:
        try:
            # Load the close price for these 10 tickers we want to trade at the end of that day
            df = pd.read_csv(os.path.join(data_folder, f"{symbol}.csv"), index_col=0, parse_dates=True)
            today_close = df.loc[date, 'Close']
            tomorrow_close = df.loc[tomorrow_date, 'Close']
            
            # Calculate the return for each ticker, sum it up for ROC
            rsi_ret += (tomorrow_close - today_close) / today_close
        except FileNotFoundError:
            print(f"File for {symbol} not found. Skipping...")
            continue
        except KeyError as e:
            print(f"Key error {e} - possible missing date in {symbol}.csv")
            continue

    for symbol in sorted_MACD:
        try:
            # Load the close price for these 10 tickers we want to trade at the end of that day
            df = pd.read_csv(os.path.join(data_folder, f"{symbol}.csv"), index_col=0, parse_dates=True)
            today_close = df['Close'][date]
            tomorrow_close = df['Close'][tomorrow_date]
            macd_ret += (tomorrow_close - today_close) / today_close
            
        except FileNotFoundError:
            print(f"File for {symbol} not found. Skipping...")
            continue
        except KeyError as e:
            print(f"Key error {e} - possible missing date in {symbol}.csv")
            continue
        

    # Compute average daily return for S&P 500
    for filename in os.listdir(data_folder):
        if filename.endswith('.csv'):
            df = pd.read_csv(os.path.join(data_folder, filename), index_col=0, parse_dates=True)
            if date in df.index and tomorrow_date in df.index:
                today_close = df['Close'][date]
                tomorrow_close = df['Close'][tomorrow_date]
                sp500_daily_return += (tomorrow_close - today_close) / today_close

    sp500_daily_return /= len(os.listdir(data_folder))
    sp500_ret_list.append(sp500_daily_return)
    

    roc_ret_list.append(roc_ret/10)
    rsi_ret_list.append(rsi_ret/10)
    macd_ret_list.append(macd_ret/10)
    
    macd_excess_return = (macd_ret / 10) - sp500_daily_return
    macd_excess_ret_list.append(macd_excess_return)
    print(i)

# Calculate the cumulative return
cumulative_roc = [roc_ret_list[0]]
for num in roc_ret_list[1:]:
    cumulative_roc.append(cumulative_roc[-1] + num)

cumulative_rsi = [rsi_ret_list[0]]
for num in rsi_ret_list[1:]:
    cumulative_rsi.append(cumulative_rsi[-1] + num)

cumulative_macd = [macd_ret_list[0]]
for num in macd_ret_list[1:]:
    cumulative_macd.append(cumulative_macd[-1] + num)

cumulative_sp500 = [sp500_ret_list[0]]
for num in sp500_ret_list[1:]:
    cumulative_sp500.append(cumulative_sp500[-1] + num)
    
cumulative_macd_excess = [macd_excess_ret_list[0]]
for num in macd_excess_ret_list[1:]:
    cumulative_macd_excess.append(cumulative_macd_excess[-1] + num)
# Plotting
# plt.plot(cumulative_roc, label="ROC Strategy", color="blue")
# plt.plot(cumulative_rsi, label="RSI Strategy", color="orange")
plt.plot(cumulative_macd, label="MACD Strategy", color="purple")
plt.plot(cumulative_sp500, label="S&P 500", color="red")
plt.plot(cumulative_macd_excess, label="MACD Excess Return", color="green")
plt.title("Performance Comparison: ROC vs RSI vs MACD vs S&P 500")
plt.xlabel("Days")
plt.ylabel("Cumulative Returns")
plt.legend()
plt.grid(True)
plt.show()
