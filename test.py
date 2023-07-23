import pandas as pd

df = pd.read_csv("sample_model_data.csv",index_col=0)

print(df)

#TODO: Implement your understanding of the backtesting algorithm here. 
for i, r in df.iterrows():
    print(i,r)
    # When you hit signals, use lists for tracking open and closed positions (i.e. their associated trade entries)
    # Check for stop loss, and take profit on the open positions
    # When closing positions, calculate and create sample performance entries