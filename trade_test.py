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

trade_config = {"user_id": None, 
            "equity_id": None, 
            "setting_id": None, 
            "date_created": None, 
            "type" : None,
            "trade_dt": None, 
            "price": None, 
            "quantity": None,
            "total": None
        }

print(market_handler.createTrade(trade_config))