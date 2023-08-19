import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, Alphavantage, Model, User

# Setup the database (and handlers) required for the system
load_dotenv() # Load ENV variables and set them down below
SQL_USER, SQL_PASS, ALPHAVANTAGE_KEY = os.getenv('MYSQL_USER'), os.getenv('MYSQL_PASS'), os.getenv('ALPHAVANTAGE_KEY') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.
# Initiate all the handlers
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main") 
user_handler = User(database=db_handler)
api_handler = Alphavantage(database=db_handler,key=ALPHAVANTAGE_KEY)
model_handler = Model(database=db_handler)
print("Loaded ENV variables and successfully initiated the DB, API, Config, and Market handlers")

user_id = user_handler.create(values=("Sample",),simple=True)

# Populate settings dictionary to be passed into Model.backtest() (NOTE: Will be user input fields on the form) 
setting_values={"user_id": user_id,
                "starting_aum": 100000, 
                "short": "EMA 5",
                "long": "SMA 15",
                "ticker": "NIO",
                "stop_loss": 10, #%
                "take_profit": 0.5,#%
                "chart_freq_mins": 0} 

# Get the price data for the setting values using the OpenFintech Alphvantage Package
df = api_handler.equity_daily(key=Alphavantage.get_key(api_handler.keys),ticker=setting_values["ticker"])
# Modify the price_data_df based on the given config values indicators section
indicators = [''.join(setting_values["short"].split(" ")),''.join(setting_values["long"].split(" "))]
df = api_handler.technical_indicator(indicators,df) # Add the tehcnical indicators data to the dataframe

# Call the backtest function with the setting along with the configuration
response = model_handler.backtest(setting_values, df)
print(response) # (NOTE: Parts of the response will be the output to be sent to the front end)

# Disconnect the database
db_handler.disconnect()
print("Disconnected database connection.")