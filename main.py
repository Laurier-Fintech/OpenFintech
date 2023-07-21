import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, User, Alphavantage, Market, Model

# Setup the database required for the system
load_dotenv()
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
data_handler = Alphavantage(database=db_handler,key=ALPHAVANTAGE_KEY)
config_handler = Model(database=db_handler)
market_handler = Market(database=db_handler)

# Set the user as the system requires (to add relational layer to the data and faciliate the automated creation of reports etc. through complex queries)
user_id = 4

# Setup the configuration/model for testing
ema_1 = 5 # Config variable 1
ema_2 = 20 # Config variable 2


# Setup the parameters for the setting
ticker = 'GOOGL'
interval = 30 #min
# NOTE: Skipping the start and end date ranges for now


# Disconnect the database
db_handler.disconnect()