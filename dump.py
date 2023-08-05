import os
import matplotlib.pyplot as plt
import pandas as pd
plt.style.use('fivethirtyeight')
from OpenFintech import Alphavantage

ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 

ticker = "HRL"
response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}")
response = response["Time Series (Daily)"]

df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]

# Create the SMA 30
df["5. SMA5"] = df["4. close"].rolling(window=5).mean()
df["6. SMA15"] = df["4. close"].rolling(window=15).mean()
print(df)

plt.figure(figsize=(12.5,4.5))
plt.plot(df["4. close"], label="Close")
plt.plot(df["5. SMA5"], label="SMA5")
plt.plot(df["6. SMA15"], label="SMA15")
plt.legend(loc ="lower right")
plt.show()

