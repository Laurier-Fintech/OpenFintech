import os 
from dotenv import load_dotenv
import mysql.connector
import sqlite3
import queries


class FinSQL:
    def __init__(self, host:str, user:str, password:str, database="sys"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.curr = self.conn.cursor()
        return
    
    def createDatabase(self, names)-> bool: # Function that can be used to create either one or many databases (requires connection)
        success=False
        try:
            # Get list of existing databases
            self.curr.execute("SHOW DATABASES")
            tables = [tableName[0] for tableName in self.curr] 
            if not isinstance(names, list): names = [names] # Convert names into a list if its just one name
            # If a database with the given name does not exist, then create it
            for name in names:
                if name not in tables: self.curr.execute(f"CREATE DATABASE {name}")
            success=True
        except Exception as e: pass # TODO: Call destructor with the Exception
        return success
    
    def insert(self, statement, values=[], many=False)-> bool :
        success=False
        try:
            if many:
                # If many values are provided, then iterate over the values and execute them with the statement (using executemany)
                if len(values)==0: raise Exception("Please provide values to insert multiple SQL entires")
                for value in values: self.curr.executemany(statement,values)
            else: self.curr.execute(statement) 
            self.conn.commit() # Commit new insertations/changes
            success=True # Update success status to return True
        except Exception as e: pass
        return success

    def disconnect(self)->bool: 
        success = True
        try:
            self.curr.close()
            self.conn.disconnect()
        except: success=False
        return success

    def __str__(self)->str:
        tables = "Tables:\n"
        self.curr.execute("SHOW DATABASES")
        for tableName in self.curr: tables+= f"\t{tableName}\n"
        return tables


if __name__=="__main__":
    load_dotenv()
    SQL_USER = os.getenv('MYSQL_USER')
    SQL_PASS = os.getenv('MYSQL_PASS') 
    host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
    handler = FinSQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    #handler.curr.execute(queries.create_users_table)
    #handler.curr.execute(queries.create_equity_table)
    #handler.curr.execute(queries.create_config_table)
    #handler.curr.execute(queries.create_setting_table)
    #handler.curr.execute(queries.create_trade_table)
    #handler.curr.execute(queries.create_performance_table)
    statement = ""
    values = [
        (),
    ]
    handler.insert( # TODO: Test and validate if its working before modifying FinData and deleting FinMongo.py

    )
    handler.disconnect()