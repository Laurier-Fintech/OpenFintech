from .Databases import MySQL
from .APIs import Alphavantage
from . import queries

# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database, market):
        self.db_handler = database
        self.market_handler = market
        return
    
    def create(self, values:dict)->int:
        # Convert the dictionary of values given by the user (which can be variable) into a set for inserting into the database
        ma_1, ma_2, ema_1, ema_2, rsi_1, rsi_2 = 0,0,0,0,0,0
        keys = values.keys()
        if "EMA" in keys:
            ema_1=values["EMA"][0]
            if len(values["EMA"])>1: ema_2=values["EMA"][1]
        if "SMA" in keys:
            ma_1=values["SMA"][0]
            if len(values["SMA"])>1: ma_2=values["SMA"][1]
        if "RSI" in keys:
            rsi_1=values["RSI"][0]
            if len(values["RSI"])>1: rsi_2=values["RSI"][1]
        values = (values["user_id"],ma_1, ma_2, ema_1, ema_2, rsi_1, rsi_2)

        # Execute MySQL statement to insert the configuration values into the AWS RDS
        self.db_handler.execute(queries.insert_configuration_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]
        
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