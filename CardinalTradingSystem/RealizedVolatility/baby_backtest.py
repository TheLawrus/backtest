from matplotlib import pyplot as plt
import pandas as pd

from utils import load_data

tickers = ["AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NVDA"]


def simp(ticker):
    data = load_data(f"data/{ticker}").resample('D')
    result = (data['close'].last() - data['close'].first()) / \
        data['close'].first()
    return result


ticker_data = {ticker: simp(ticker) for ticker in tickers}
################################################################################
combined_df = pd.concat(ticker_data.values(), axis=1,
                        keys=ticker_data.keys()).dropna()
combined_df['Mean'] = combined_df.mean(axis=1)
sp500 = combined_df['Mean'].cumsum(axis=0).tolist()
sp500.insert(0, 0)
################################################################################
df = pd.read_csv("factor.csv", index_col=0).dropna()
df['max'] = df.idxmax(axis=1)

val = [0]
for idx, row in df.iterrows():
    ticker = row['max']
    val.append(ticker_data[ticker].loc[idx] + val[-1])
################################################################################
plt.figure(figsize=(8, 7))
plt.plot(val, label='Factor VAL', color='red')
plt.plot(sp500, label='S&P 500 VAL', color='blue')
plt.title('Return / Realized Volatility')
plt.xlabel('"AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NVDA"')
plt.ylabel('Portfolio Value')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
