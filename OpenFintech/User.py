from Databases import SQL
import queries

class User(SQL): # Used to handle the user data 
    def __init__(self):
        # Creates table if it does not exist already 
        return
    
    def createUser(self,values=[], multiple=True):
        # Create simple or full user
        if isinstance(values, set): self.execute(queries.insert_simple_user, values=values)
        else: self.execute(queries.insert_full_user, values=None)
        return
    
    def readUser():
        return

    def updateUser():
        return
    
    def deleteUser():
        return
