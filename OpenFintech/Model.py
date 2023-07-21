from .Databases import MySQL
from . import queries

# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database=None):
        self.db_handler = database
        return
    
    def create(self, values:set)->int:
        try:
            self.db_handler.execute(queries.insert_configuration_entry, values)
            query_last = "SELECT LAST_INSERT_ID();"
            config_id = self.db_handler.execute(query_last, query=True)[0][0]
        except:
            print("Error: Could not insert configuration into configuration table. Check if User ID is provided")
            return -1
        
        return config_id

    def createSetting(self,values):
        try:
            self.db_handler.execute(queries.insert_setting_entry, values)
            query_last = "SELECT LAST_INSERT_ID();"
            config_id = self.db_handler.execute(query_last, query=True)[0][0]
        except:
            print("Error: Could not insert configuration into configuration table. Check if User ID is provided")
            return -1
        
        return config_id

    # The testing and running of configuation relies on the Market model.
    def backtest(self, setting:dict, configuration:dict) -> dict:
        print("\nModel.backtest():")
        # Import the configuration information from the given ID and set it as a dictionary if only the ID was given
        if len(configuration)>1: pass # Create the config and update the dict to just be {"ID": config_id}

        # Create a entry to the settings table
        setting_id = self.createSetting(values=(setting["user_id"],configuration["config_id"],setting["ticker"],
                                   setting["stop_loss"],setting["starting_aum"],setting["take_profit"],
                                   setting["chart_freq_mins"]))
        print(f"\tCreated setting with the ID {setting_id}")
        
        # Import the data for given the setting using the given data_handler (Alphavantage object)
        # Add the 




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
    
    def simulate(self): # NOTE: We can worry about this after we build backtest
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        # This would use realtime price data which would be added to (or retrived from) the appropriate collection or database or dataframe in market
        # It would perform the required calculations based on the confiurations
        
        # Realtime (simualted) testing code here

        # This would take a setting and a configuration as well
        # It should output performance and market data (including price data) as pandas df or a list of dictionaries?
        return

    # Prints the market overview specific to the model and configurations. (can use SQL complex queries and create visualizations now)
    def __str__(self):
        return("working")