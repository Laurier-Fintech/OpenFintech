import os 
import logging 
from pymongo import MongoClient, errors

# NOTE: These todo points will be converted to tickets and added to the Notion workspace
# -> TODO: Set logger levels for terminal and file output. Test logger.
# -> TODO: Implement FinMongo.__str__
# -> TODO: Add virutal database functionality 

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

    def __init__(self, host: str):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - Constructs a new 'FinMongo' object and establishes a connection to the MongoDB server.
        
        -----------------------------------------------------------
        Parameters
        -----------------------------------------------------------
        - host (str): The host connection string for MongoDB.
        
        -----------------------------------------------------------
        Raises
        -----------------------------------------------------------
        - ConnectionFailure: If the connection to the MongoDB server fails.
        """
        # Setup logger
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Establish connection with mongo cluster
        try:
            self.client = MongoClient(host) # host connection string
            self.client.server_info()  # force connection request for testing 
        except errors.ConnectionFailure: self.logger.exception("Could not connect to MongoDB (Error: Connection Failure).")   
        else: self.logger.info("MongoDB Connection Successful.")
            
        return

    def connect(self):
        """
        -----------------------------------------------------------
        Purpose
        -----------------------------------------------------------
        - A placeholder for handling multiple connections. 
        - This method is not yet implemented.
        """
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
        # sample_info = {'version': '6.0.6', 'gitVersion': '26b4851a412cc8b9b4a18cdb6cd0f9f642e06aa7', 'modules': ['enterprise'], 'allocator': 'tcmalloc', 'javascriptEngine': 'mozjs', 'sysInfo': 'deprecated', 'versionArray': [6, 0, 6, 0], 'bits': 64, 'debug': False, 'maxBsonObjectSize': 16777216, 'storageEngines': ['devnull', 'ephemeralForTest', 'inMemory', 'queryable_wt', 'wiredTiger'], 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1686251487, 4), 'signature': {'hash': b'\x0b\xcc*\xc1\x81\xd9\xebv\x06\xcc\xc05\x9e+\t\xfe&\x1d\xab)', 'keyId': 7204913445559336962}}, 'operationTime': Timestamp(1686251487, 4)}
        # TODO: Take the sample info and create a string with the important sections for the user
        # TODO: (Alternative) Can show other information like the databases, collections, collection metrics (num of documents) and so on
        return str(self.client.server_info())


if __name__ == "__main__": 
    MONGODB_PWD = os.environ.get('MONGODB_PWD') 
    # TODO: Need to add the ENV PWD to the URL (was experiencing bugs earlier)
    handler = FinMongo("mongodb+srv://OpenFintech:yT6KHkhVcvHQ42AX@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority") #TODO: Add ENV var handling functionality

    # TODO: Code to test the DB wrapper
    
    handler.disconnect() # Disconnect the handler (and the MongoDB client) after use