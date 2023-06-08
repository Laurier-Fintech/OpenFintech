import os 
import logging 
# Need to set level (do it now so we can set it as a standard for the rest)
from pymongo import MongoClient, errors

class FinMongo:
    def __init__(self, host: str):
        # TODO: Setup Logger (look into learning Python logger) for outputting to the terminal (and file?)
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        # Establish connection with mongo cluster
        try:
            self.client = MongoClient(host) # host connection string
            self.client.server_info()  # force connection request for testing 
        except errors.ConnectionFailure: self.logger.exception("Could not connect to MongoDB (Error: Connection Failure).")   
        else: self.logger.info("MongoDB Connection Successful.")
            
        return

    def connect(self): #NOTE: For handling multiple connections
        return

    def disconnect(self):
        if self.client: 
            try: self.client.close()
            except: self.logger.error("Failed to close the connection.")
            else: self.logger.info("Sucessfully closed the connection.")
        return

    def __str__(self): # Print the status (connection overview) and other information
        #sample_info = {'version': '6.0.6', 'gitVersion': '26b4851a412cc8b9b4a18cdb6cd0f9f642e06aa7', 'modules': ['enterprise'], 'allocator': 'tcmalloc', 'javascriptEngine': 'mozjs', 'sysInfo': 'deprecated', 'versionArray': [6, 0, 6, 0], 'bits': 64, 'debug': False, 'maxBsonObjectSize': 16777216, 'storageEngines': ['devnull', 'ephemeralForTest', 'inMemory', 'queryable_wt', 'wiredTiger'], 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1686251487, 4), 'signature': {'hash': b'\x0b\xcc*\xc1\x81\xd9\xebv\x06\xcc\xc05\x9e+\t\xfe&\x1d\xab)', 'keyId': 7204913445559336962}}, 'operationTime': Timestamp(1686251487, 4)}
        # TODO: Take the sample info and create a string with the important sections for the user
        # TODO: (Alternative) Can show other information like the databases, collections, and collection metrics (num of documents) and so on
        return str(self.client.server_info())


if __name__ == "__main__": 
    MONGODB_PWD = os.environ.get('MONGODB_PWD') 

    handler = FinMongo("mongodb+srv://OpenFintech:yT6KHkhVcvHQ42AX@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority") #TODO: Add ENV var handling functionality

    # Testing code
    
    handler.disconnect() # Disconnect the handler (and the MongoDB client) after use