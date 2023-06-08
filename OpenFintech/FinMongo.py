# Libaries and Env Vars
import os
import logging
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_PWD = os.environ.get('MONGODB_PWD') # cluster password

# MongoDB Database Client --> 
class Mongo_Client:
    def __init__(self, host: str):

        # Establish connection with mongo cluster
        try:
            self.client = MongoClient(host) # host connection string
            self.client.server_info()  # force connection request for testing 
            self.logger.info("MongoDB Connection Successful.") #NOTE: Using loger without setting it up (levels)
        except ConnectionFailure: 
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

