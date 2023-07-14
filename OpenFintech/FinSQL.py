import os 
from dotenv import load_dotenv
import mysql.connector
import sqlite3


class FinSQL:
    def __init__(self, host:str=None, user:str=None, password:str=None, database:str=None):
        self.inmemory = False
        if host!=None:
            if user==None or password==None or database==None: raise Exception("username, password, or database cannot be none if the host is provided to establish a MySQL connection.")
            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
        else:
            self.conn = sqlite3.connect(":memory:")
            self.inmemory=True
        self.curr = self.conn.cursor()
        return
    
    def disconnect(self)->bool: 
        success = True
        try:
            self.curr.close()
            self.conn.disconnect()
        except: success=False
        return success

    def __str__(self)->str:
        if not self.inmemory: 
            tables = "Tables:\n"
            self.curr.execute("SHOW DATABASES")
        else: 
            tables = response = f"Connected to in-memory db: {self.conn}"
        for tableName in self.curr: tables+= f"\t{tableName}\n"
        return tables



if __name__=="__main__":
    load_dotenv()
    SQL_USER = os.getenv('MYSQL_USER')
    SQL_PASS = os.getenv('MYSQL_PASS') 
    host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
    handler = FinSQL(host=host,user=SQL_USER,password=SQL_PASS)
    print(handler)
    handler.disconnect()