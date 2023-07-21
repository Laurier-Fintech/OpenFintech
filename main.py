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
data_handler = Alphavantage(database=db_handler,key=ALPHAVANTAGE_KEY)
model_handler = Model(database=db_handler)
market_handler = Market(database=db_handler)
print("Loaded ENV variables and successfully initiated the DB, API, Config, and Market handlers")

# Set the user as the system requires (to add relational layer to the data and faciliate the automated creation of reports etc. through complex queries)
user_id = 4 # TODO: Update user_handler.create() to return the created entry's ID

# Setup the configuration/model for testing
ema_1 = 5 # Config variable 1
ema_2 = 20 # Config variable 2
ma_1,ma_2,rsi_1,rsi_2=0,0,0,0 # Set missing values as zero
config_values = (user_id, ma_1, ma_2, ema_1, ema_2, rsi_1, rsi_2)
config_id = model_handler.create(config_values) # Create the config using the handler (and store the ID for creating other entries in other related tables)
print(f"Created {config_values} configuration with the ID {config_id}")

# Setup the parameters for the setting NOTE: Skipping the start and end date ranges for now as they're not required
ticker = 'GOOGL'
interval = 30 #mins
stop_loss = 10 #%
take_profit = 10 #%

# Call the backtest function with the setting along with the configuration
model_handler.backtest(setting={"ticker":ticker,"interval":30, "stop_loss":stop_loss,"take_profit":take_profit}, configuration={"ID":config_id})

# Disconnect the database
db_handler.disconnect()