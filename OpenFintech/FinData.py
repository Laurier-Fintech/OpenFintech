from utilities import create_logger
from FinMongo import FinMongo
# Unique (customized) impelmentation of the Alphavantage wrapper to support OpenFintech (mainly Model.test_config and Model.run_config in Model.py)
# Data required for Model.test_config is pulled from the market
# Esentially, FinData give data to the market which is then used by models?

# For testing config, we mainly need the following data
    # Price Data for company x for y date range in z chart frequency

# We could potentially store the data the wrapper collects in a database/collection
# The goal would be to reduce key usage by using existing data and refreshing stored data preemptively.
# We should move the Alphavantage wrapper in here and pack it in with a new name and redesign it to suit this system (for the classes/functions mentioned above)
# We would also have to reference the wrapper in the Market component as the data for settings are esentially required by the market not the model in and of itself.

class FinData:
    def __init__(self, database=None, logger=None, key="", keys=[]):
        # Setup logger
        if logger==None: logger=create_logger("market")
        self.logger = logger
        # Create a database 
        self.inmemory = False
        if database==None:
            self.mongo = FinMongo()
            self.inmemory = True
            database = self.mongo.client["db"]
        self.database = database
        # Create the required equity and crypto collections
        self.equities = self.database["equities"]
        self.crypto = self.database["crypto"]
        # Setup key/keys
        self.key = key # Is empty if the user provided a list of keys
        self.keys = {key: 0 for key in keys} 

        if len(self.keys)==0 and self.key=="": raise Exception("Please provide an Alphavantage key or a list of Alphavantage keys.")


        # Setup endpoints


        # Have endpoint URLs stored here for simpliciy
        # Required endpoints:
        # Company overview (our own get equity function) <- possibly have a equity object
        # Crypto Overview (???????)

        return
    
    def _get_key(): # Internal access only
        return


    @staticmethod 
    def _request(url:str): 
        # Has error handling for our own request module 
        return
    

if __name__=="__main__":
    # Load OS variables for DB
    print("In Main")