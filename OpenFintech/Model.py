from .Databases import MySQL
from .APIs import Alphavantage
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

    def createSetting(self,values:dict):
        # Convert values dict to a set
        values=(values["user_id"],values["config_id"],values["ticker"],
                                            values["stop_loss"],values["starting_aum"],values["take_profit"],
                                            values["chart_freq_mins"])
        self.db_handler.execute(queries.insert_setting_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]
        return config_id

    # The testing and running of configuation relies on the Market model.
    def backtest(self, setting_values:dict, config_values:dict, api_handler:Alphavantage) -> dict:
        print("\nModel.backtest():")
        # Create the configuration entry using this objects method
        config_id = self.create(config_values)

        setting_values["config_id"] = config_id # Add the config_id to the setting (since these values will be passed onto the database)
        # Create a entry to the settings table
        setting_id = self.createSetting(setting_values)
        print(f"\tCreated setting with the ID {setting_id}")
        
        # Import the data for given the setting using the given api_handler (Alphavantage object)
        df = api_handler.equity_intraday(api_handler.key,setting_values["ticker"],interval=setting_values["chart_freq_mins"])
        print("\tPrice Data:")
        print(df)

        # Modify the price_data based on the given config values
        indicators = {"SMA":[10],"EMA":[10,20]}
        df = api_handler.technical_indicator(indicators,df)
        print("After manipulating the dataframe with technical_indicator() method:")
        print(df)


        # NOTE: (OLD, go based of your understanding from todays meeting) Algorithm/Loop to test the configuration 
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