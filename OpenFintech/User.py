from .Databases import MySQL
from . import queries

class User(): # Used to handle the interactions with the Users table 
    def __init__(self, database:MySQL):
        self.db_handler = database
        return
    
    def create(self, values:set, simple=True)->bool: # TODO: Add multiple feature as well
        success = False
        if simple: success = self.db_handler.execute(queries.insert_simple_user, values=values)
        else: success = self.db_handler.execute(queries.insert_complete_user, values)
        return success
    
    def read(): # Given the read values, bind them and perform the query
        return

    def update(): # Given the update values, bind them and perform the operation
        return
    
    def delete(): # Delete the given user_id or username (since they are unique and contain the cascade property, MySQL will do most of the overhead work)
        return

if __name__=="__main__":
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    SQL_USER = os.getenv('MYSQL_USER')
    SQL_PASS = os.getenv('MYSQL_PASS') 
    host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
    db_handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    user_handler = User(db_handler)

    success = user_handler.create(("David","test@mylaurier.ca","12@test", "3","computer science",),simple=False)
    print(success)
    db_handler.disconnect()