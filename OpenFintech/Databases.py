import sqlite3

class SQLite3:
    def __init__(self, name=":memory:"):
        self.conn:sqlite3.Connection = sqlite3.connect(name)
        self.curr = self.conn.cursor()
        return
    
    def execute(self,statement, query=False, values:dict={}):
        if len(values)>0: self.curr.execute(statement,values)
        else: self.curr.execute(statement)
        self.conn.commit()
        if query: result = self.curr.fetchall() 
        else: result = self.curr.lastrowid
        return result
    
    def download(self):
        return 
    
    def disconnect(self):
        try: self.conn.commit()
        except: pass
        self.curr.close()
        self.conn.close()
        return 