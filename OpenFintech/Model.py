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