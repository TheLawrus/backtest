import pickle
import pandas as pd

with open("AAPL", "rb") as fp:   # Unpickling
    aggs = pickle.load(fp)

# Extracting the 5min closing prices from the list
closing_prices = [agg.close for agg in aggs]

# Calculate the 5-minute returns
returns = [(closing_prices[i] - closing_prices[i-1]) / closing_prices[i-1] for i in range(1, len(closing_prices))]

# Calculate the realized volatility for each 5-minute interval based on the squared returns
# Note: This gives you the 5-minute realized volatility, not annualized or daily
realized_volatilities = [((sum(returns[max(0, i-77):i])**2)/78)**0.5 for i in range(1, len(returns)+1)]

# Construct a DataFrame to save the data to CSV
df = pd.DataFrame({
    'Timestamp': [agg.timestamp for agg in aggs][1:],  # Starting from the second entry because the first doesn't have a return
    'Realized_Volatility': realized_volatilities
})

# Save to CSV
df.to_csv('realized_volatility.csv', index=False)

# Annualize the realized volatility
N = 78  # Number of 5-minute intervals in a trading day
T = 252  # Number of trading days in a year
annualized_volatilities = [vol * (N * T)**0.5 for vol in realized_volatilities]

# Construct a DataFrame to save the data to CSV
df = pd.DataFrame({
    'Timestamp': [agg.timestamp for agg in aggs][1:],  
    'Annualized_Realized_Volatility': annualized_volatilities
})

# Save to CSV
df.to_csv('annualized_realized_volatility.csv', index=False)

# Risk Adjusted Return
RAR = [returns[i] / annualized_volatilities[i] if annualized_volatilities[i] != 0 else 0 for i in range(len(returns))]

# Construct a DataFrame to save the data to CSV
df = pd.DataFrame({
    'Timestamp': [agg.timestamp for agg in aggs][1:],  
    'Annualized_Realized_Volatility': annualized_volatilities,
    '5min_Return': returns,
    'Risk_Adjusted_Return': RAR
})

# Save to CSV
df.to_csv('factor_data.csv', index=False)