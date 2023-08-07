import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, User, Alphavantage, Market, Model

# Setup the database (and handlers) required for the system
load_dotenv() # Load ENV variables and set them down below
SQL_USER, SQL_PASS, ALPHAVANTAGE_KEY = os.getenv('MYSQL_USER'), os.getenv('MYSQL_PASS'), os.getenv('ALPHAVANTAGE_KEY') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.

# Initiate all the handlers
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
user_handler = User(database=db_handler)
api_handler = Alphavantage(database=db_handler,key=ALPHAVANTAGE_KEY)
market_handler = Market(database=db_handler)
model_handler = Model(database=db_handler, market=market_handler)
print("Loaded ENV variables and successfully initiated the DB, API, Config, and Market handlers")

# Populate settings dictionary to be passed into Model.backtest()
setting_values={"user_id": 1, # TODO: Update user_handler.create() to return the created entry's ID
                "starting_aum": 100000, 
                "short": "EMA 5",
                "long": "SMA 10",
                "ticker": "MXI", # NOTE: Popped in backtest
                "stop_loss": 10, #%
                "take_profit": 0.0025} #%

# Call the backtest function with the setting along with the configuration
#model_handler.backtest(setting_values, api_handler)

# Disconnect the database
db_handler.disconnect()
print("Disconnected database connection.")