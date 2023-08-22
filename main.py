import os 
from dotenv import load_dotenv
from OpenFintech import Model

load_dotenv() # Load ENV variables and set them down below
# Populate settings dictionary to be passed into Model.backtest() (NOTE: Will be user input fields on the form) 
setting_values={"user_id": 1,
                "starting_aum": 100000, 
                "short": "EMA 5",
                "long_": "SMA 15",
                "ticker": "AAPL",
                "stop_loss": 0.05, #%
                "take_profit": 0.5,#%
                "chart_freq_mins": 0} 
handler = Model("Test.db")
# Call the backtest function with the setting along with the configuration
response = handler.backtest(setting_values, os.getenv('ALPHAVANTAGE_KEY'))
handler.handler.disconnect() # Closes the database

print(response) # (NOTE: Parts of the response will be the output to be sent to the front end)