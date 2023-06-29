from .utilities import create_logger
from .FinMongo import FinMongo

# Data required for Model.test_config is pulled from the market
# Esentially, FinData give data to the market which is then used by models?

# For testing config, we mainly need the following data
    # Price Data for company x for y date range in z chart frequency

# We could potentially store the data the wrapper collects in a database/collection
# The goal would be to reduce key usage by using existing data and refreshing stored data preemptively.
# We should move the Alphavantage wrapper in here and pack it in with a new name and redesign it to suit this system (for the classes/functions mentioned above)

class FinData:
    def __init__(self, database=None, logger=None, key="", keys=[]):
        
        # Setup logger if required
        if logger==None: logger=create_logger("market")
        self.logger = logger
        
        # Create a database if required
        self.inmemory = False
        if database==None:
            self.mongo = FinMongo()
            self.inmemory = True
            database = self.mongo.client["db"]
        self.database = database
        
        # Create the required equity and crypto collections if they do not exist already, else simply connect
        self.equities = self.database["equities"]
        self.crypto = self.database["crypto"]
        
        # Setup key/keys
        self.key = key # Is empty if the user provided a list of keys
        self.keys = {key: 0 for key in keys} 
        if len(self.keys)==0 and self.key=="": raise Exception("Please provide an Alphavantage key or a list of Alphavantage keys.")
        if len(self.keys)==0 and self.key!="": self.keys[self.key]=0 # NOTE: From this point on, only self.keys will be used.

        return
    
    # TODO:
    # Write a function for each "endpoint"
    # Each function would check the collection for the data, if available and within x period, send the data
    # Else, use the sattic get_key() and the static request method to get the data
    # If an error occured, send the old data and handle the key

    # Equity overview's refresh rate should defaultly be set to 30 days (roughly a month) (TODO: Add to __init__)
    def overview(self): # NOTE: Currently works for equities only as supported by Alphavantage
        key = self.get_key(self.keys)
        # Check the collection for the data, if available and within x period, send the data
        

        # Else, use the sattic get_key() and the static request method to get the data
        # If an error occured, send the old data and handle the key
        return

    @staticmethod
    def get_key(keys:dict):
        if len(keys)==0: raise Exception("No keys given.")
        key = min(keys, key=keys.get)
        keys[key]+=1
        return key

    @staticmethod 
    def _request(url:str): 
        # Has error handling for our own request module 
        return

if __name__=="__main__":
    # Load OS variables for DB
    print("In Main")
