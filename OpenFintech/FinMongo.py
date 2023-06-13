import logging
import pymongo_inmemory
from pymongo import MongoClient, errors
from utilities import create_logger
# TODO: Finish __str__
# TODO: Add CRUD features (with returns optionally in Pandas DF's)


class FinMongo:
    """ 
    -----------------------------------------------------------
    Purpose
    -----------------------------------------------------------
    - A class used to represent a MongoDB connection handler.
    
    -----------------------------------------------------------
    Attributes
    -----------------------------------------------------------
    - host (str): a string containing the host connection string for MongoDB
    - logger (Logger): a logger object used for logging connection and disconnection events
    - client (MongoClient): a MongoClient object that maintains the connection to the MongoDB server
    """

    def __init__(self, host: str = None, logger:logging.Logger = None):

        if logger==None: logger = create_logger("finmongo")
        self.logger=logger
                
        if host==None:
            # If no host connection str was given, create and return an in-memory database
            self.client = pymongo_inmemory.MongoClient()
            self.logger.info("Successfully created a in-memory MongoDB.")
        else:
            # Establish connection with mongo cluster
            try:
                self.client = MongoClient(host) # host connection string
                self.client.server_info()  # force connection request for testing 
            except errors.ConnectionFailure:
                self.logger.exception("Could not connect to MongoDB (Error: Connection Failure).")   
            else: 
                self.logger.info("Successfully connected to MongoDB.")
            
        return

    def connect(self):
        # This function would be built to switch hosts or handle multiple connections
        return

    def disconnect(self):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Closes the connection to the MongoDB server.

        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - None

        -----------------------------------------------------------
        Returns
        -----------------------------------------------------------
        - Success (bool): True if the connection was successfully closed, False otherwise.

        -----------------------------------------------------------
        Raises
        -----------------------------------------------------------
        - Exception: If an exception occurred while closing the connection.
        """
        success = False
        if self.client: 
            try: self.client.close()
            except: self.logger.error("Failed to close the connection.")
            else: 
                self.logger.info("Sucessfully closed the connection.")
                success = True
        return success

    def __str__(self): # Print the status (connection overview) and other information
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Returns a string representation of the MongoDB server's status and other information.
        
        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - None
        
        -----------------------------------------------------------
        Returns
        -----------------------------------------------------------
        - str: A string with the MongoDB server's information.
        """
        # sample_info_server_not_in_memory = {'version': '6.0.6', 'gitVersion': '26b4851a412cc8b9b4a18cdb6cd0f9f642e06aa7', 'modules': ['enterprise'], 'allocator': 'tcmalloc', 'javascriptEngine': 'mozjs', 'sysInfo': 'deprecated', 'versionArray': [6, 0, 6, 0], 'bits': 64, 'debug': False, 'maxBsonObjectSize': 16777216, 'storageEngines': ['devnull', 'ephemeralForTest', 'inMemory', 'queryable_wt', 'wiredTiger'], 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1686251487, 4), 'signature': {'hash': b'\x0b\xcc*\xc1\x81\xd9\xebv\x06\xcc\xc05\x9e+\t\xfe&\x1d\xab)', 'keyId': 7204913445559336962}}, 'operationTime': Timestamp(1686251487, 4)}
        # TODO: Take the sample info and create a string with the important sections for the user
        # TODO: (Alternative) Can show other information like the databases, collections, collection metrics (num of documents) and so on
        return str(self.client.server_info())

if __name__ == "__main__": 
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS') 
    handler = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority")     
    #handler = FinMongo() # in-memory
    client = handler.client

    # Code to test db, collection, and document creation
    # In MongoDB, db's and collections are not created untill they have data added to them
    mydb = client["mydatabase"]
    mycol = mydb["users"]
    sample_data = {
        "date_created": None,
        "user_id": 3, "username": "Brown",
        # For analytical purposes
        "major":"CS", "year": 30,
        "email": None, "password": None
    }

    x = mycol.insert_one(sample_data)

    print(client.list_database_names())
    print(mydb.list_collection_names())
    print(x.inserted_id)
    
    handler.disconnect() # Disconnect the handler (and the MongoDB client) after use