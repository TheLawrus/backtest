from functools import reduce
import pandas as pd
import matplotlib.pyplot as plt
import pickle
from datetime import datetime

factor_df = pd.read_csv('AV.csv')
# Convert the 'Date' column to datetime format
factor_df['Date'] = pd.to_datetime(factor_df['Date'])

stocks = ["AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NVDA"]

dfs = []
for stock in stocks:
    print(stock)
    with open(f"data/{stock}", "rb") as fp:
        aggs = pickle.load(fp)

    daily_closing_prices = pd.DataFrame({
        'Date': [datetime.utcfromtimestamp(agg.timestamp / 1000).date() for agg in aggs],
        stock: [agg.close for agg in aggs]
    })
    
    daily_closing_prices['Date'] = pd.to_datetime(daily_closing_prices['Date'])

    daily_closing_prices = daily_closing_prices.groupby('Date').agg({
        stock: lambda x: ((x.iloc[-1] - x.iloc[0]) /
                          x.iloc[0]) if len(x) > 1 else 0
    }).reset_index()

    # Append the DataFrame to the list
    dfs.append(daily_closing_prices)

closing_prices_df = reduce(lambda left, right: pd.merge(
    left, right, on='Date', how='outer'), dfs)
closing_prices_df['Mean_Percent_Change'] = closing_prices_df[stocks].mean(
    axis=1)


#################################################################
########################### FACTORS###############################
#################################################################
# Drop the date column for now, as we want to compare only the 'ticker*' columns
df_numeric = factor_df.drop('Date', axis=1)

# Number of largest columns to find
n_largest = 1  # You can change this value

# Find the n largest columns in each row
n_largest_columns_list = df_numeric.apply(
    lambda row: row.nsmallest(n_largest).index.tolist(), axis=1)

# Create new columns to store the names of the n largest columns
factor_df['largest_columns'] = n_largest_columns_list

computed_means = []
for idx, row in factor_df.iterrows():
    date = row['Date']
    largest_tickers = row['largest_columns']

    # Find the corresponding row in the second DataFrame
    row2 = closing_prices_df.loc[closing_prices_df['Date'] == date]

    # Compute the mean for the largest tickers
    mean_value = row2[largest_tickers].iloc[0].mean()
    computed_means.append(mean_value)

closing_prices_df['Mean_Factor_Change'] = computed_means

# print(closing_prices_df)

#################################################################
############################## PLOT###############################
#################################################################
sp500 = [0]
factor = [0]

for i in closing_prices_df['Mean_Percent_Change']:
    sp500.append(i + sp500[-1])

for i in closing_prices_df['Mean_Factor_Change']:
    factor.append(i + factor[-1])

# Plotting
plt.figure(figsize=(14, 7))
plt.plot(sp500, label='SP500 VAL', color='blue')
plt.plot(factor, label='Factor VAL', color='red')

plt.title('Portfolio Performance Comparison')
plt.xlabel('Date')
plt.ylabel('Portfolio Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
