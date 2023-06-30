from .utilities import create_logger
from .FinMongo import FinMongo
# TODO:
# Trade CRUD Functions
# Implement __str__ to provide an overview of the market

class Market: # Provides simulated backtesting and real-time testing functionalities.

    def __init__(self, database=None, logger=None):
        
        if logger==None: logger=create_logger("market")
        self.logger = logger

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

    # TODO: Backtesting (NOTE: Use the ERD and other CRUD functions for reference. Keep default parameters in mind. Feel free to create static methods if you need)
    def create_trade(self):
        return
    def read_trade(self):
        return
    def update_tade(self):
        return
    def delete_trade(self):
        return
    
    # Realtime (Provides simulated running functionality) NOTE: Ignore these for now
    def open_position(self):
        return
    def close_position(self):
        return
    def update_position(self):
        return
    def view_position(self):
        return

    # Close database and cleanup
    def close(self):
        if self.inmemory==True: self.mongo.disconnect()
        return
    
    # For providing an overview of the market
    def __str__(self):
        return
