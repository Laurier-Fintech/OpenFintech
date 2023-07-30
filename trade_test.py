import os
from dotenv import load_dotenv
from OpenFintech import MySQL, queries

load_dotenv() # Load ENV variables and set them down below
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
ALPHAVANTAGE_KEY = os.getenv('ALPHAVANTAGE_KEY') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.
print("called object")
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")


db_handler.curr.execute(queries.create_users_table)
db_handler.curr.execute(queries.create_equity_table)
db_handler.curr.execute(queries.create_config_table)
db_handler.curr.execute(queries.create_setting_table)
db_handler.curr.execute(queries.create_trade_table)
db_handler.curr.execute(queries.create_performance_table)

db_handler.disconnect()
print("Working")