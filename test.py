import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sample_model_data.csv",index_col=0)
df['open_position'] = False
df['profit'] = 0
df['signal'] = None
open_position_price = df['4. close'][0];

#TODO: Implement your understanding of the backtesting algorithm here. 
for i, r in df.iloc[1:].iterrows():
    # When you hit signals, use lists for tracking open and closed positions (i.e. their associated trade entries)
    # Check for stop loss, and take profit on the open positions
    # When closing positions, calculate and create sample performance entries
    # When you hit the end of the data, close all open positions and calculate the final performance
    if df['SMA_10'][i] > df['EMA_20'][i] and df['SMA_10'][i - 1] < df['EMA_20'][i - 1]:
        df.at[i, 'signal'] = 'buy'
        if df.at[i - 1, 'open_position'] == False:
            df.at[i, 'open_position'] = True
            open_position_price = df['4. close'][i]

    elif df['SMA_10'][i] < df['EMA_20'][i] and df['SMA_10'][i - 1] > df['EMA_20'][i - 1]:
        df.at[i, 'signal'] = 'sell'
        if df.at[i - 1, 'open_position'] == True:
            df.at[i, 'open_position'][i] = False
            df.at[i, 'profit'] = df['4. close'][i] - open_position_price + df['profit'][i - 1]

    else:
        df.at[i, 'signal'] = 'hold'

for i in range(len(df)):
    print(df['signal'][i])
    print(df['profit'][i])