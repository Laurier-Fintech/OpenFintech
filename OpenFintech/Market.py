from datetime import datetime as dt
# TODO:
# Trade CRUD Functions
# Implement __str__ to provide an overview of the market

class Market: # Provides simulated backtesting and real-time testing functionalities.

    def __init__(self, database=None):
        return

    # Creates a query given some kind of ID --> reduce redundancy?
    @staticmethod
    def create_query(self)->dict:
        config_id = int(input("Enter Config ID ( > 0):"))
        if config_id == None | config_id <0:
            raise Exception("Error: Invalid Config ID")
        return {"config_id": config_id}

    def read_trade(self, query: dict={}) -> list:
        if len(query) == 0: query = self.create_query()
        result = list(self.trades.find(query))
        return result

    def update_trade(self, query:dict={}, values: dict={}, many = False) -> int:

        return
    
    def delete_trade(self, query: dict={}, many = False):

        return

    # Close database and cleanup
    def close(self):
        if self.inmemory==True: self.mongo.disconnect()
        return
    
    # For providing an overview of the market
    def __str__(self):
        return