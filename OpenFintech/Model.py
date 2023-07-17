from .Market import Market
# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database=None):
        return
    
    def create_model():
        # Terminal user interface to create the model 
        # Create configuration and setting based on user input
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

    # Prints the market overview specific to the model and configurations. (can use SQL complex queries and create visualizations now)
    def __str__(self):
        return "working"