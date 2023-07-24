from . import queries

# TODO:
# Trade CRUD Functions
# Implement __str__ to provide an overview of the market (easier and more useful with MySQL)
# Implement methods in Market to create performance entires


class Market: # Provides simulated backtesting and real-time testing functionalities.

    def __init__(self, database=None):
        return
    
    def createTrade(self, trade_configs: dict)->int:
        return_values = {"user_id": None, 
                          "equity_id": None, 
                          "setting_id": None, 
                          "date_created": None, 
                          "type" : None,
                          "trade_dt": None, 
                          "price": None, 
                          "quantity": None,
                          "total": None}
        
        for key in trade_configs.keys():
            return_values[key] = trade_configs[key]
        
        values = set(return_values.keys())
        
        self.db_handler.execute(queries.insert_trade_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        trade_id = self.db_handler.execute(query_last, query=True)[0][0]

        return trade_id
    
    def readTrade():
        return
    
    def updateTrade():
        return
    
    def deleteTrade():
        return
    
    # For providing an overview of the market
    def __str__(self):
        return