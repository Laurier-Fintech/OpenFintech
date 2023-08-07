import os
from dotenv import load_dotenv
from OpenFintech import MySQL, queries

load_dotenv()
SQL_USER, SQL_PASS = os.getenv('MYSQL_USER'), os.getenv('MYSQL_PASS')
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")

db_handler.execute(statement=queries.create_users_table)
db_handler.execute(statement=queries.create_equity_table)
db_handler.execute(statement=queries.create_setting_table)
db_handler.execute(statement=queries.create_trade_table)
db_handler.execute(statement=queries.create_performance_table)

db_handler.disconnect()