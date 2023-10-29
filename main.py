import os 
from dotenv import load_dotenv
from OpenFintech import Model
import pandas as pd
import matplotlib.pyplot as plt

load_dotenv() # Load ENV variables and set them down below
# Populate settings dictionary to be passed into Model.backtest() (NOTE: Will be user input fields on the form) 
setting_values={"user_id": 1,
                "starting_aum": 100000, 
                "short": "EMA 5",
                "long_": "SMA 15",
                "ticker": "GOOGL",
                "stop_loss": 0.05, #%
                "take_profit": 0.5,#%
                "chart_freq_mins": 0} 
handler = Model()
# Call the backtest function with the setting along with the configuration
response = handler.backtest(setting_values, os.getenv('ALPHAVANTAGE_KEY'))
handler.handler.disconnect() # Closes the database


print(response)

df: pd.DataFrame = response["price_data"]

print(df)

# Set general graph properties (the dates are used as the default X domain)
plt.figure(figsize=(12, 6))

# Add the data to the graph
plt.plot(df['4. close'], label='Close', marker='o', color='blue')
plt.plot(df[f'6. {setting_values["short"].replace(" ", "")}'], label=setting_values["short"].replace(" ", ""), linestyle='--', color='red')
plt.plot(df[f'7. {setting_values["long_"].replace(" ", "")}'], label=setting_values["long_"].replace(" ", ""), linestyle='--', color='green')

# Finish adding general graph properties (that may act on price data) and ..
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show() # Display the graph 

print(response["trade_data"])

# TODO: Save the graph as a JPEG (as this system will be used to simplify the graph displaying process)