from datetime import datetime
import pickle
import pandas as pd

# List of stocks to process
stocks = ["AAPL", "AMZN","GOOG", "GOOGL", "MSFT", "NVDA"]

# Initialize an empty DataFrame for storing the final factor data
result_df = pd.DataFrame()

for stock in stocks:
    # Load data for each stock
    with open(f"data/{stock}", "rb") as fp:
        aggs = pickle.load(fp)
        
    # Extracting the 5min closing prices from the list
    closing_prices = [agg.close for agg in aggs]
    # Calculate the 5-minute returns
    returns = [(closing_prices[i] - closing_prices[i-1]) / closing_prices[i-1] for i in range(1, len(closing_prices))]
    # Calculate the realized volatility for each 5-minute interval based on the squared returns
    realized_volatilities = [((sum(returns[max(0, i-77):i])**2)/78)**0.5 for i in range(1, len(returns)+1)]
    # Annualize the realized volatility
    N = 78  # Number of 5-minute intervals in a trading day
    T = 252  # Number of trading days in a year
    annualized_volatilities = [vol * (N * T)**0.5 for vol in realized_volatilities]
    # Risk Adjusted Return
    RAR = [returns[i] / annualized_volatilities[i] if annualized_volatilities[i] != 0 else 0 for i in range(len(returns))]

    # Construct a DataFrame for the current stock's data
    df = pd.DataFrame({
        'Date': [datetime.utcfromtimestamp(agg.timestamp / 1000).date() for agg in aggs][1:],  # Convert to date format
        'Annualized_Realized_Volatility': annualized_volatilities,
        '5min_Return': returns,
        'Risk_Adjusted_Return': RAR
    })

    # Calculate the average Risk Adjusted Return for the day for this stock
    daily_RAR = df.groupby('Date').mean()['Risk_Adjusted_Return']

    # Append this stock's RAR to the result_df
    if result_df.empty:
        result_df = pd.DataFrame(daily_RAR).rename(columns={'Risk_Adjusted_Return': stock})
    else:
        result_df = result_df.join(pd.DataFrame(daily_RAR).rename(columns={'Risk_Adjusted_Return': stock}), on='Date')

# Save the combined results to CSV
result_df.reset_index().to_csv('AV.csv', index=False)