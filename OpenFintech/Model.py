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

    def test_config(self):
        # Each test is also a session of its own. This session ID is what's used with the market component for tracking trades. 
        return
    
    def run_config(self):
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        return


if __name__=='__main__':
    pass