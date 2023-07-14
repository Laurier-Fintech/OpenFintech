import os 
from dotenv import load_dotenv
import mysql.connector
import sqlite3
import queries


class FinSQL:
    def __init__(self, host:str=None, user:str=None, password:str=None, database="sys"):
        self.inmemory = False
        if host!=None:
            if user==None or password==None: raise Exception("username and password cannot be none if the host is provided to establish a MySQL connection.")
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
    
    def createDatabase(self, names):
        if self.inmemory==True: raise Exception("FinSQL.createDatabase does not support inmemory databases.")
        self.curr.execute("SHOW DATABASES")
        tables = [tableName[0] for tableName in self.curr]
        if not isinstance(names, list): names = [names]
        for name in names:
            if name not in tables: self.curr.execute(f"CREATE DATABASE {name}")
        return
    
    def insert(self, statement, values=[], many=False):
        if self.inmemory==True: raise Exception("FinSQL.insert does not support inmemory databases.")
        if many:
            if len(values)==0: raise Exception("Please provide values to insert multiple SQL entires")
            for value in values: self.curr.executemany(statement,values)
        else: self.curr.execute(statement)
        self.conn.commit()
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
    handler = FinSQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    handler.curr.execute(queries.create_equity_table)
    handler.disconnect()