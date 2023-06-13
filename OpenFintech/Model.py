from utilities import create_logger
from FinMongo import FinMongo

class Model:

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger("model")

        if database==None:
            self.mongo = FinMongo()
            database = self.mongo.client["db"]

        self.database = database
        self.positions = self.database["positions"]
        self.trades = self.database["trades"]
        return

    def create_config(self):
        return
    
    def read_config(self):
        return

    def update_config(self):
        return
    
    def delete_config(self):
        return

    # The testing and running of configuation relies on the Market model.
    def test_config(self):
        # Each test is also a session of its own. This session ID is what's used with the market component for tracking trades. 
        return
    
    def run_config(self):
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        return

    # Prints the market overview specific to the model and configurations.
    def __str__(self):
        return

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

