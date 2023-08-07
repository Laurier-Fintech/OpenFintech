# TODO: Add the stop loss and take profit systems into place in the holding section of the logic
# TODO: Update the intraday function in Alphvatange class and add other price data functions as required
# TODO: Update the indicator function in Alphavnatage class to be simplified and also review the "mapping" implementation that allows for package flexibility
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
for i, r in df.iterrows():
    # Get the data for the current row (datestamp)
    date, close, base, upper = i, r["4. close"], r["5. EMA5"], r["6. SMA10"]

    # Check the order of base and upper
    #print(date, close, base, upper)

    if base>upper and open==False:
        purchase_price = close
        quantity = aum / purchase_price # max purchasable shares
        total = purchase_price * quantity # total cost
        aum -= total # remove cost from balance (should come out to 0 rn by default but leaving formula in)
        print(i, ": Buy", purchase_price, aum)
        open = True
    elif base<upper and open==True: # NOTE: Should we handle sells that lead to profits or losses differently ?
        sale_price = close
        total = quantity * sale_price # Get the total gained from the sale
        quantity = 0 # Update the quantity NOTE: Since this is our hypothetical market, when we sell, we assume we find a perfect buyer for all the shares we own at the closing price
        aum += total # add the total gained from the sale to the total 
        # Differentitate between sales that lead to profits vs losses and handle each case (NOTE: Possible room for future iteration's projects)
        profitable = False if sale_price<purchase_price else True
        print(i, ": Sell", sale_price, aum, profitable)
        if profitable: print("\tProfit Captured Per Share Sold: ", sale_price-purchase_price) # If profitable, output the profit captured per share sold
        open = False
    else:
        #print(i,": Hold")
        pass

plt.show()