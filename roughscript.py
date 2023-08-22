import os 
from dotenv import load_dotenv
from OpenFintech import Model,Alphavantage

load_dotenv() # Load ENV variables and set them down below
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY')

# Populate settings dictionary to be passed into Model.backtest() (NOTE: Will be user input fields on the form) 
setting_values={"user_id": 1,
                "starting_aum": 100000, 
                "short": "EMA 5",
                "long_": "SMA 15",
                "ticker": "TSLA",
                "stop_loss": 0.10, #%
                "take_profit": 0.5,#%
                "chart_freq_mins": 0} 

# Get the price data for the setting values using the OpenFintech Alphvantage Package
df = Alphavantage.equity_daily(key=ALPHAVANTAGE_KEY,ticker=setting_values["ticker"])
# Modify the price_data_df based on the given config values indicators section
indicators = [''.join(setting_values["short"].split(" ")),''.join(setting_values["long_"].split(" "))]
df = Alphavantage.technical_indicator(indicators,df) # Add the tehcnical indicators data to the dataframe

handler = Model("Test.db")
# Call the backtest function with the setting along with the configuration
response = handler.backtest(setting_values, df)
print(response) # (NOTE: Parts of the response will be the output to be sent to the front end)


handler.handler.disconnect() # Closes the database