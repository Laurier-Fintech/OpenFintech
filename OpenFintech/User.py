#TODO: 

class User:
    def __init__(self, db_client=None):
        if db_client==None:
            # Setup a virtual database here using FinMongo
            # Set the virtual database as the db_client
            pass

        # Pass User ID as a property
        self.id = None
        # So users can connect directly to their user (entry)
        #  given a connection and use the component accordingly
        return

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value:int):
        # TODO: Error handling around ID
        # Checks if the value is the right
        return


    # General properties of the user
    def create(self):
        # Creates a user and then returns their ID
        return
    
    def delete(self):
        return
    
    def update(self):
        return