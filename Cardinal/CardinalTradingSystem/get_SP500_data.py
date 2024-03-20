# # Import yfinance 
# import yfinance as yf   
 
# # Get the data for the stock Apple by specifying the stock ticker, start date, and end date 
# data = yf.download('AAPL','2016-01-01','2018-01-01') 
 
# # Plot the close prices 
# import matplotlib.pyplot as plt 
# data.Close.plot() 
# plt.show() 
# data.to_csv('AAPL.csv')
import yfinance as yf
import pandas as pd

# Define the ticker symbols for the S&P 500 index
ticker_symbols = ['^GSPC']

# Set the start and end date for data retrieval
start_date = "2018-01-01"
end_date = "2023-03-05"

# Loop through the ticker symbols and retrieve stock market data using yfinance
for symbol in ticker_symbols:
    ticker_data = yf.download(symbol, start=start_date, end=end_date)

    # Convert the retrieved data to a Pa
    # 
    # 
    # 
    # ndas DataFrame
    df = pd.DataFrame(ticker_data)

    # Write the DataFrame to a CSV file in the local directory
    df.to_csv(f"{symbol}.csv")

