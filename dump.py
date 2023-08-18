# TODO: Update backtest.py implementation based on test.py and to match the flow of inputs from the now update main.py file
# TODO: Review for other changes (such as the one based on the note left below) and add visualization as an optional variable (along with this implementation) to the backtest function so the plot is outputted with the terminal data for the user of the package to study and play around with 
# NOTE: Tracking quantity might be useless now (adding more complexity for the team maybe) because we just buy everything we can and sell everything we can, the AUM and quantity is cool from a user/case study point of view tho (and maybe gives room for more market maker style projects in the future)

import os
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('fivethirtyeight')
from OpenFintech import Alphavantage

ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 

ticker = "MXI"
response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}")
response = response["Time Series (Daily)"]

df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]

# Create the required indicators
df["5. EMA5"] = df["4. close"].ewm(span=3, adjust=False).mean()
df["6. SMA10"] = df["4. close"].rolling(window=10).mean()
df.dropna(inplace=True)
print(df)

plt.figure(figsize=(12.5,4.5))
plt.plot(df["4. close"], label="Close")
plt.plot(df["5. EMA5"], label="EMA5")
plt.plot(df["6. SMA10"], label="SMA10")
plt.legend(loc ="lower right")

aum = 100000
open = False 
quantity = 0 # shares currently in possession
purchase_price = 0
sale_price = 0
stop_loss = 10#%
take_profit = 0.0025#%

for i, r in df.iterrows():

    # Get data from the current row (unit of time)
    date, close, short, long = i, r["4. close"], r["5. EMA5"], r["6. SMA10"]

    if open==False: # At the current unit of time, if there are no open positions....

        if short>long: # Check if the short term mean (base) has passed the long term mean (upper), indicating a upwards change in the price action and a buy signal
            purchase_price = close # store the purchase price in a variable initialized outside the loop (for referencing in future iterations)
            quantity = aum / purchase_price # Calculate the maximum purchaseable shares (NOTE: This is a limitation of the current system by design)
            total = purchase_price * quantity # Calculate the total cost of the purchase 
            aum -= total # remove cost from balance (NOTE: leaving formula in although this would always be zero due to the limitation highlighted above)
            print(i, ": Buy @", purchase_price, " AUM:", aum)
            open = True # Update variable to indicate that a purchase has been made, i.e. position opened.
    
    else: # When there is an open position.... 
        
        sell = False #NOTE: This boolean variable is used as a trigger to avoid creating a sell function and to avoid writing redundant code

        if short<long: sell = True # If the short term mean has fell underneath the long term mean, indicating a downwards change in the price action, triger the sale of all open positions (NOTE: "all" due to the limitation of the system as discussed earlier)

        else: # When holding, check if the current price, relative to the purchase price, triggers a stop loss or take profit
            if (close <= (purchase_price - (purchase_price*stop_loss))): sell = True # Conditional statement for stopping loss
            if (close >= (purchase_price + (purchase_price*take_profit))): sell = True # Conditional statement for taking profit

        if sell: # Code to sell open positions/current holdings (transaction)
            sale_price = close
            total = quantity * sale_price # Get the total gained from the sale
            quantity = 0 # Update the quantity NOTE: Since this is our hypothetical market, when we sell, we assume we find a perfect buyer for all the shares we own at the closing price
            aum += total # add the total gained from the sale to the aum 
            # Differentitate between sales that lead to profits vs losses and handle each case differently (NOTE: Potential room for a future project)
            profitable = False if sale_price<purchase_price else True
            print(i, ": Sell for", sale_price, " AUM:",aum, " Profitable: ",profitable)
            if profitable: print("\tProfit Captured Per Share Sold: ", sale_price-purchase_price) # If profitable, output the profit captured per share sold
            open = False

print(f"Final AUM: {aum}")
plt.show()