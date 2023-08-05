import os
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('fivethirtyeight')
from OpenFintech import Alphavantage

ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 

ticker = "AAPL"
response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}")
response = response["Time Series (Daily)"]

df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]

# Create the SMA 30
df["5. SMA5"] = df["4. close"].rolling(window=5).mean()
df["6. SMA15"] = df["4. close"].rolling(window=15).mean()
df.dropna(inplace=True)
print(df)

plt.figure(figsize=(12.5,4.5))
plt.plot(df["4. close"], label="Close")
plt.plot(df["5. SMA5"], label="SMA5")
plt.plot(df["6. SMA15"], label="SMA15")
plt.legend(loc ="lower right")
plt.show()

aum = 100000


# NOTE: Requires us to track the open positions so we can calculate the success of the strategy

open = False 
for i, r in df.iterrows():
    # Get the data for the current row (datestamp)
    date, close, base, upper = i, r["4. close"], r["5. SMA5"], r["6. SMA15"]

    # Check the order of base and upper
    #print(date, close, base, upper)

    if base>upper and open==False:
        print(i, ": Buy")
        open = True
    elif base<upper and open==True:
        print(i, ": Sell")
        open = False
    else:
        print(i,": Hold")
    




# Implement the mean reversion strategy/trading algorithm to simulate a high-frequency trader
# If SMA5 > SMA 15
    # Buy as many shares (on the closing price) as you can with the aum and update the aum
# If SMA15 < SMA5
    # Sell
    # Clear


# buy: simulate the process of creating a trade order (calculating the numbers)
#   the trade date, closing price, quantity, and total (which is how much we spent on this order)
#   quantity = quantity of purchase = aum/closing price
#   total = quantity * closing price
#   aum -= total # subtract the value of the purchase from the AUM

# sell: simulate the process of selling when a sell signal is hit
#   update the AUM with the sale value