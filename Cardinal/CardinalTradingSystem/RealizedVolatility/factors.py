from utils import load_data
import pandas as pd


def getFactor1(ticker):
    df = load_data(f"data/{ticker}")

    # calculate daily returns
    df['returns'] = df['close'].pct_change().fillna(0)

    # calculate squared returns
    df['squared_returns'] = df['returns'] ** 2

    # calculate daily realized variance
    daily_rv = df.resample('D')['squared_returns'].sum()

    # annualized realized volatility
    arv = (daily_rv * 252) ** .5

    # daily max difference
    result = df.resample('D')['squared_returns'].agg(
        lambda x: x.max() - x.min())

    # annualized max difference? idk what this is called
    return result/arv

def generateFactorList(factor_function):
    tickers = ["AAPL", "AMZN", "GOOG", "GOOGL", "META", "MSFT", "NVDA"]
    factor_data = [(ticker, factor_function(ticker)) for ticker in tickers]

    df = pd.DataFrame()
    for ticker, factor_series in factor_data:
        df[ticker] = factor_series

    return df

generateFactorList(getFactor1).to_csv("factor.csv")
