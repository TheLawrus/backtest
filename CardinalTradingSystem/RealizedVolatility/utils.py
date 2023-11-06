import pickle
import pandas as pd

def load_data(path):
    with open(path, "rb") as fp:   # Unpickling
        aggs = pickle.load(fp)

    data = [
        {
            'open': agg.open,
            'high': agg.high,
            'low': agg.low,
            'close': agg.close,
            'volume': agg.volume,
            'vwap': agg.vwap,
            'timestamp': pd.to_datetime(agg.timestamp, unit='ms'),
            'transactions': agg.transactions,
            'otc': agg.otc
        }
        for agg in aggs
    ]

    df = pd.DataFrame(data)

    # Convert the timestamp to datetime and set it as the index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    return df