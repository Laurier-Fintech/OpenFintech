import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, Alphavantage, Market, Model

# Setup the database required for the system
load_dotenv()
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com" #NOTE: Host address is set to the OpenFintech AWS Server.
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")

# Set the user as the system requires (to add relational layer to the data and faciliate the automated creation of reports etc. through complex queries)


# Setup the configuration/model for testing


# Setup the parameters for the setting


# Disconnect the database
db_handler.disconnect()