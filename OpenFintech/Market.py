"""
Pre-text Information:
Additionally, it can also provide our own market 
analysis and reports based on position and trade 
information.

Requires Model.py to be built out as it needs 
to handle configuration information.
"""
from datetime import datetime as dt
from utilities import create_logger
from FinMongo import FinMongo

class Market: # Provides simulated backtesting and real-time testing functionalities.

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger(f"{dt.now()} market.log")

        if database==None:
            self.mongo = FinMongo()
            database = self.mongo.client["db"]

        self.database = database
        self.positions = self.database["positions"]
        self.trades = self.database["trades"]
        return

    # Realtime (Provides simulated running functionality)
    def open_position(self):
        return
    
    def close_position(self):
        return
    
    def update_position(self):
        return
    
    def view_position(self):
        return

    # Backtesting 
    def create_trade(self):
        return
    
    def read_trade(self):
        return
    
    def update_tade(self):
        return
    
    def delete_trade(self):
        return
    
    # Close database and cleanup
    def close(self):
        success = self.mongo.disconnect()
        return success
    
    # For providing an overview of the market
    def __str__(self):
        # Maybe we can have a simulated market maker fee
        return


if __name__=='__main__':
    trade = {
        "date_created":None, 
        "trade_dt":None,
        # Composite primary key for identifying this document (for future reference)
        "user_id":None, 
        "config_id":None,
        # For identifying the trade and its related session
        "session_id":None, 
        "trade_id":None, 
        # Trade information
        "ticker":None, 
        "type":None, 
        "price":None, 
        "quantity":None, 
        "total":None
    }

    market = Market()
    market.close()