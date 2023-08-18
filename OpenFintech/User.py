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
