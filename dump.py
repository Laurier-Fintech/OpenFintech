#NOTE: File used to create and handle simple database stuff during development
import os 
from dotenv import load_dotenv
from OpenFintech import MySQL, User

load_dotenv()
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
user_handler = User(db_handler)

success = user_handler.create(("David","test@mylaurier.ca","12@test", "3","computer science",),simple=False)
print(success)
db_handler.disconnect()