import os 
import logging 
# Need to set level (do it now so we can set it as a standard for the rest)
from pymongo import MongoClient, errors
MONGODB_PWD = os.environ.get('MONGODB_PWD') # cluster password

# MongoDB Database Client --> 
class FinMongo:
    def __init__(self, host: str):
        # Setup Logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Establish connection with mongo cluster
        try:
            self.client = MongoClient(host) # host connection string
            self.client.server_info()  # force connection request for testing 
            self.logger.info("MongoDB Connection Successful.")
        
        except errors.ConnectionFailure: 
            self.logger.exception("Could not connect to MongoDB.") # Add the error code    

    # Seperate method for connecting (possible server resource management)?
    def connect(self):
        pass

    def disconnect(self):
        if self.client: self.client.close()

    def __str__(self): # Print the status (connection overview) and other information
        return


# Database
# contains a list of "collections" objects
class database:
    
    pass

# Mongo Collection (Table) --> User, etc...
# collection.insert_doc() 
class collection:
    pass

if __name__ == "__main__": 
    # client = MongoClient(connection_string)

    # dbs = client.list_database_names()
    # print(dbs)

    mongo_client = Mongo_Client("mongodb+srv://OpenFintech:yT6KHkhVcvHQ42AX@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority")

