from utilities import create_logger
from FinMongo import FinMongo

class Market: # Provides simulated backtesting and real-time testing functionalities.

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger("market")

        self.inmemory = False
        if database==None:
            self.mongo = FinMongo()
            self.inmemory = True
            database = self.mongo.client["db"]

        self.database = database
        self.positions = self.database["positions"]
        self.buffer = {} # NOTE: {{open_position: awaiting signal,..} -> Replaced with associated closing position before being registered as a trade # NOTE: This is something to take into consideration when designing the ERD for the system/software
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
        if self.inmemory==True: self.mongo.disconnect()
        return
    
    # For providing an overview of the market
    def __str__(self):
        # Maybe we can have a simulated market maker fee
        return


if __name__=='__main__':
    sample_trade = {
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