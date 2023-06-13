from utilities import create_logger
from FinMongo import FinMongo
from Market import Market

class Model:

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger("model")

        self.inmemory = False
        if database==None:
            self.mongo = FinMongo()
            self.inmemory = True
            database = self.mongo.client["db"]

        self.database = database
        self.market = Market(self.database,logger)
        self.configs = self.database["configurations"]
        self.setting = self.database["setting"]
        return

    def create_config(self):
        # TODO:
        # Check the values of the configuration to make sure they are valid, raise exceptions where required <- Possible validation function
        # Log success or faliure
        # Check if the configuration is not in configurations already
        # If no data is given, take the required values from the users from the terminal
        # Add the configuration to the database
        # Return the configuration ID that was assigned to the one that was added
        return
    
    def read_config(self):
        return

    def update_config(self):
        # Would be relying on the same validation function for configuration
        return
    
    def delete_config(self):
        return

    # The testing and running of configuation relies on the Market model.
    def test_config(self, setting:dict = {}, configuration:dict={}) -> dict:
        # Each test is also a session of its own. This session ID is what's used with the market component for tracking trades. 
        # Outside of the configuration, this also requires the appropriate setting data
        # Setting can be a seperate collection


        # Code to test the configuration with the setting
        # This will also include code that uses the Alphavantage wrapper Laurier Fintech offers
        # We will be customizing the Alphavantage wrapper for this usecase as well
        # This will require a restructure and modification
        # We could potentially store the data the wrapper collects.
        # The goal would be to reduce key usage by using existing data and refreshing stored data preemptively.
        # We should move the Alphavantage wrapper in here and pack in with a new name and redesign it to suit this system
        # and we would have to reference the wrapper in the Market component.

        # Code to save the performance of the test with the configuration and the setting


        # Return the performance as a dictionary        
        # If it fails, return the failure as a dictionary

        # NOTE:
        # Have a optional variable to get the history (data) as well.
        # This would be something we'd have to get from the database
        # It can be something we pack into the market
        # What would the return datatype be
        return
    
    def run_config(self):
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        # This would use realtime price data which would be added to (or retrived from) the appropriate collection or database or dataframe in market
        # It would perform the required calculations based on the confiurations
        
        # Realtime (simualted) testing code here

        # This would take a setting and a configuration as well
        # It should output performance and market data (including price data) as pandas df or a list of dictionaries?
        return

    # Database disconnecting, marketing handling, and cleanup where required
    def close(self):
        self.market.close()
        if self.inmemory==True: self.mongo.disconnect()     
        return

    # Prints the market overview specific to the model and configurations.
    def __str__(self):
        return "working"


if __name__=='__main__':

    sample_configuration = {	
    "date_created":None, 
    # Composite Primary Key
    "user_id":None, "config_id":None, 
    # General Configuration 
    "stop_loss":None, "take_profit":None, "AUM":None, 
    # SMA Strat. Config.
    "MaPeriod1":None, "MaPeriod2":None,
    # MACD Strat. Config.
    "EmaPeriod1":None, "EmaPeriod2":None,
    # RSI Strat. Config.
    "RsiLength":None, "MaLength":None
    }

    sample_performance = {
	"date_created":None, 
	
	"config_id":None, "session_id":None, 
	
	"chart_frequency":None, "date_range":None,

	"starting_aum":None, "ending_aum":None, 
	"percent_change":None, "dollar_change":None, 
    "num_trades":None, "avg_hold_time":None,

    "avg_change_in_balance_per_trade":None, 
    }

    model = Model()
    print(model)
    model.close()
