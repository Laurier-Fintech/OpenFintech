import os 
from dotenv import load_dotenv
import mysql.connector
import queries

class MongoDB: # TODO: Simplified implementation of our FinMongo code
    def __init__():
        return

class SQL:
    def __init__(self, host:str, user:str, password:str, database:str):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.curr = self.conn.cursor()
        return

    # Function that can execute statements with no values, one value, or multiple values (regardless of create, delete, etc as long as it follows MySQL's prepared statement conventions and packs multiple values in a list of sets and single entry values in just a set)
    def execute(self, statement, values=[], multiple=False)-> bool :
        
        success=False
        try:
            # For handling multiple values that need to be binded to the prepared (and passed) statement/query before being executed
            if multiple:
                # If many values are provided, then iterate over the values and execute them with the statement (using executemany)
                if len(values)==0: raise Exception("Please provide values to insert multiple SQL entires.")
                for value in values: self.curr.executemany(statement,value)
            
            # For handling statements/queries that have no values or one set of values
            else: 
                if len(values)==0: self.curr.execute(statement)  # When no values are given, simply call execute
                
                else:
                    # Check if the given values are in a set (required by MySQL connector)
                    if isinstance(values, tuple)!=True: raise Exception("Given values must be in a set to be executed.")
                    self.curr.execute(statement,values) # Bind values to statement and execute

            self.conn.commit() # Commit new insertations/changes
            success=True # Update success status to return True
            
        except Exception as e: 
            print(e) # Can call destructor or handle error differently in the future
            pass

        return success

    # Function that closes the currsor and disconnects the MySQL connection
    def disconnect(self)->bool: 
        success = True
        try:
            self.curr.close()
            self.conn.disconnect()
        except: success=False
        return success

    # Function that returns the list of tables in the database
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
    handler = SQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    #handler.curr.execute(queries.create_users_table)
    #handler.curr.execute(queries.create_equity_table)
    #handler.curr.execute(queries.create_config_table)
    #handler.curr.execute(queries.create_setting_table)
    #handler.curr.execute(queries.create_trade_table)
    #handler.curr.execute(queries.create_performance_table)
    success = handler.execute( # TODO: Validate with inserting users, equities, configs, settings, trades, and performance
        queries.insert_simple_user, values=("Harri",)
    )
    print(success)
    handler.disconnect()