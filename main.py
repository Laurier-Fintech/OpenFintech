import os 
from dotenv import load_dotenv


load_dotenv()
SQL_USER = os.getenv('MYSQL_USER')
SQL_PASS = os.getenv('MYSQL_PASS') 
host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
db_handler = MySQL(host=host,user="admin",password="$5svXm!6NAFIL5U",database="main")
model_handler = Model(db_handler)

success = model_handler.create(('1', 2, 3, 4, 5, 6, 7))
print(success)
db_handler.disconnect()