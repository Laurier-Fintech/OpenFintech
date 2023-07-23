import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, User, Alphavantage, Market, Model

# Setup the database (and handlers) required for the system
load_dotenv() # Load ENV variables and set them down below
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.

# Initiate all the handlers
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
api_handler = Alphavantage(database=db_handler,key=ALPHAVANTAGE_KEY)
market_handler = Market(database=db_handler)
model_handler = Model(database=db_handler, market=market_handler)
print("Loaded ENV variables and successfully initiated the DB, API, Config, and Market handlers")

# Set the user as the system requires (to add relational layer to the data and faciliate the automated creation of reports etc. through complex queries)
user_id = 4 # TODO: Update user_handler.create() to return the created entry's ID
config_values={
    "user_id":user_id,
    "EMA":[20],
    "SMA":[10]
}

# Setup the parameters for the setting NOTE: Skipping the start and end date ranges for now as they're not required
starting_aum = 1000000 # USD
ticker = 'GOOGL'
interval = 30 #mins
stop_loss = 10 #%
take_profit = 10 #%
setting_values={"user_id": user_id,"starting_aum": starting_aum, 
                "ticker":ticker,"chart_freq_mins":30, 
                "stop_loss":stop_loss,"take_profit":take_profit}

# Call the backtest function with the setting along with the configuration
model_handler.backtest(setting_values, config_values, api_handler)

# Disconnect the database
db_handler.disconnect()
print("Disconnected database connection.")