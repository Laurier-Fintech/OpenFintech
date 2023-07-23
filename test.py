import pandas as pd
# Create unit tests for everything
# (Using this as a test file for building out the algorithm)

df = pd.read_csv("sample_model_data.csv",index_col=0)

print(df)

for i, r in df.iterrows():
    print(i,r)


# NOTE: (OLD, go based of your understanding from todays meeting) Algorithm/Loop to test the configuration 
# Iterate over the pandas df (that contains the price and indicator data)
# When a signal for opening is hit (based on the configuration)
#   Open a position
#   Add trade to the buffer and add signal:position pair to a list for close checking
# When a signal for closing is hit (based on the config and positions)
#   Close the associated open position
#   Register the trade
# Clear open positions and prepare trade log
    # Given the trade and market data, calculate the performance data

    # Return the market, positions, trades, and performance data.
    # Some of these can be returned optionally.