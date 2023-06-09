import pymongo_inmemory

# The user class will be packaged into ____
# Users of our package can use this class for handling USER CRUD and other features for Fintech applications

class User:
    def __init__(self, db_client=None):

        if db_client==None:
            # Setup a virtual database here using FinMongo
            # Set the virtual database as the db_client
            db_client = pymongo_inmemory.MongoClient()  # No need to provide host

        # Pass User ID as a property so users can connect directly to their profile
        self.id = None

        return

    @property 
    def id(self):
        # Also used as the getter
        return self._id
    
    @id.setter
    def id(self, value:int):
        # TODO: Error handling around ID
        # Checks if the value is the right
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