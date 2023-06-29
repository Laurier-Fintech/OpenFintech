from .utilities import create_logger
from .FinMongo import FinMongo
from .Market import Market
# TODO:
# Configuration CRUD functions
# Add referential integrity validation where required (possibly create a _validate function)
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger("model")

        self.inmemory = False
        if database==None:
            self.mongo = FinMongo()
            self.inmemory = True
            database = self.mongo.client["db"]

        self.database = database
        self.market = Market(self.database,logger) # The market object provides our model package with the ability to close/open positions and register trades
        # NOTE: For the collections we create, we have to manually maintain referential integrity where/when needed.
        self.configs = self.database["configurations"] # This collection will contain information such as the lengths and periods of the indicators for the models we provide.
        self.setting = self.database["setting"] # This collection will contain information such as the date range, chart frequency, and the stop-loss/take-profit for a test/run relative to a configuration. 
        self.history = self.database["history"]
        self.performance = self.database["performance"] 
        return

    def create_config(self): # Save information such as the length and period 
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

        # Tests for configurations are performed with settings.
        # Each test requires a settings which i.e. represents a session.
        # Settings need to be stored relative to a configuration.
        # Settings are collections in and of itself.

        # NOTE: Algorithm/Loop to test the configuration 
        # Provide the setting to the market to get the required (price) data as a pandas df
        # Perform the required calculations and add the required indicators (for the given configuration) to the pandas df
        # Add the pandas df to the database (to the appropriate collection)
        # Iterate over the pandas df (that contains the price and indicator data)
        # When a signal for opening is hit (based on the configuration)
        #   Open a position
        #   Add trade to the buffer and add signal:position pair to a list for close checking
        # When a signal for closing is hit (based on the config and positions)
        #   Close the associated open position
        #   Register the trade
        # Clear open positions and prepare trade log


        # Given the trade and market data, calculate the performance data


        # Return the market, positions, trades, and performance data.
        # Some of these can be returned optionally.
        return
    
    def run_config(self): # NOTE: We can worry about this after we build test_config
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
