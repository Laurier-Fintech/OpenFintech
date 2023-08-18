from .Databases import MySQL
from .APIs import Alphavantage
from . import queries
import copy

# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database, market):
        self.db_handler = database
        self.market_handler = market # is this still required? Also, this has db_handler so do we really need to ask for extra db_handler?
        return
    
    def create(self,values:dict): # Function used to create a settings entry
        # Convert values dict to a set
        values=(values["user_id"],values["equity_id"], values["short"], values["long"],
                values["stop_loss"],values["take_profit"],values["starting_aum"],
                values["chart_freq_mins"])
        self.db_handler.execute(queries.insert_setting_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]
        return config_id

    # The testing and running of configuation relies on the Market model.
    def backtest(self, setting_values:dict, api_handler:Alphavantage) -> dict:
        print("\nModel.backtest():")

        # Replace ticker with the equity_id
        ticker = setting_values.pop("ticker") # Remove ticker from the setting_values dict
        response = api_handler.overview(ticker) # Retrive its last appropriate entry from the db (or request data from Alphavantage and create entry in DB)
        setting_values["equity_id"] = response[0] # Add the equity_id to the setting_values dict
        
        # Create a entry to the settings table
        setting_id = self.create(setting_values)
        print(f"\tCreated setting with the ID {setting_id}")

        # Import the data for given the setting using the given api_handler (Alphavantage object)
        df = Alphavantage.equity_daily(key=Alphavantage.get_key(api_handler.keys), ticker=ticker)
        print("\tPrice Data:")
        print(df)

        # Modify the price_data_df based on the given config values indicators section
        df = api_handler.technical_indicator({setting_values["short"],setting_values["long"]},df)
        print(df)
        
        #print("Total buy signals generated:", signals_count)

        #df.to_csv("sample_model_data.csv", encoding='utf-8') 
        # Check test.py for the implementation

        # Calculate performance data and create performance entry
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