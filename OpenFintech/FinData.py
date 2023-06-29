import requests
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
    def overview(self, ticker:str): # NOTE: Currently works for equities only as supported by Alphavantage
        key = self.get_key(self.keys)
        # Check the collection for the data, if available and within x period, send the data
        result = self.equities.find_one({"ticker": ticker})
        if result==None:
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={key}"
            response = self._request(url)
            print(response)
            # Add the entry to the collection
            # If it fails, loop back
        # Check if its over the limit, if so then request data

        return

    # Close database and cleanup
    def close(self):
        if self.inmemory==True: self.mongo.disconnect()
        return

    # Internal utility functions (can be used externally as well as they are esentially independent from the package (no self parm.))
    @staticmethod
    def get_key(keys:dict):
        if len(keys)==0: raise Exception("No keys given.")
        key = min(keys, key=keys.get)
        keys[key]+=1
        return key

    @staticmethod 
    def _request(url:str): 
        # Has error handling for our own request module 
        response = requests.get(url)
        # Check if the request's response is valid/if it failed
        if response.status_code==200: # Check if the request worked 
            try: response = response.json()
            except: 
                raise Exception("Failed to convert response to JSON.")
            else:
                if "Note" not in response.keys(): 
                    return response
                else: 
                    raise Exception("Exceeded request limit")
        raise Exception(f"Request Failed {response.status_code}")