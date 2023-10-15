import pandas as pd
import matplotlib.pyplot as plt


rsi_df = pd.read_csv('RSI.csv')

ret_list = []
for i in range(14, 100):#1300
    ret = 0
    date = rsi_df['Date'][i]
    tomorrow_date = rsi_df['Date'][i+1]

    sorted_RSI = rsi_df.iloc[i][1:].sort_values().dropna()[:10].index
    for symbol in sorted_RSI:
        df = pd.read_csv(f"C:/Users/15104/Documents/Cardinal/CardinalTradingSystem/Data/{symbol}.csv", index_col=0, parse_dates=True)
        today_close = df['Close'][date]
        tomorrow_close = df['Close'][tomorrow_date]
        ret += (tomorrow_close - today_close) / today_close 
        
    ret_list.append(ret/10)
    print(i)

cumulative_sum = [ret_list[0]]
for num in ret_list[1:]:
    cumulative_sum.append(cumulative_sum[-1] + num)

plt.plot(cumulative_sum)
plt.show()