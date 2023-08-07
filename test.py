import os
import pandas as pd
from OpenFintech import Alphavantage

ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 

ticker = "MXI"
response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={ALPHAVANTAGE_KEY}")
response = response["Time Series (Daily)"]

df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]

config_values={
    "short": "ema 5", #NOTE: Should be converted to lower before processing
    "long_": "sma 10"
}

# Extract the type of indicator along with its period as int
short = config_values["short"].split(" ")
short_period,short = int(short[1]), short[0]
long_ = config_values["long_"].split(" ")
long_period, long_ = int(long_[1]), long_[0]

# Compute the short and long term mean cols and add them to the database
df[f"5. {short} {short_period}"] = df["4. close"].rolling(window=short_period).mean() if short=="sma" else df["4. close"].ewm(span=short_period, adjust=False).mean()
df[f"6. {long_} {long_period}"] = df["4. close"].rolling(window=long_period).mean() if short=="sma" else df["4. close"].ewm(span=long_period, adjust=False).mean()
