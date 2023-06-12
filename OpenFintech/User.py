from FinMongo import FinMongo

# The user class will be packaged into ____
# Users of our package can use this class for handling USER CRUD and other features for Fintech applications

class User:
    def __init__(self):
        # Pass User ID and Host as a property so users can connect directly to their profile
        self._id = None
        self._host = None
        return

    @property 
    def id(self):
        # Also used as the getter
        return self._id
    
    @property
    def host(self):
        # Can add other layers of checks before returning (such as the user's access level)
        return self._host


    @id.setter
    def id(self, value:int):
        if value<0: raise Exception("Invalid ID. ID should be > 0")
        self._id = value
        return

    @host.setter
    def host(self,host:str):
        self._host = FinMongo(host)
        return

    # User(s) CRUD functions
    def create(self):
        # Creates a user and then returns their ID(s) to the user 
        return
    
    def delete(self):
        # Given a ID, or a set of IDs, or a JSON with the approprite data, remove the user from the system
        # Perform any calculations, error handling, raise exceptions as required, 
        return
    
    def update(self):
        # Update user profile(s) given JSON information
        return
    

if __name__=='__main__':
    handler = User()
    # Set host as None to create a in-memory Finmongo DB.
    # This allows users to test the package without creating a server for the DB
    handler.host=None 
    handler.host.disconnect()


    print("Disconnected")