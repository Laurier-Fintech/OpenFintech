from .utilities import create_logger
from datetime import datetime as dt
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
    def _validate(self, data: dict) -> bool:
        valid = True
        # User ID
        if data["user_id"]==None | data['user_id']<0: 
            valid = not valid
            self.logger.error("Invalid User ID, must be zero or positive.")
            raise Exception("Invalid User ID, must be zero or positive.")
        
        # Equity ID
        if data["equity_id"]==None | data['equity_id']<0: 
            valid = not valid
            self.logger.error("Invalid Equity ID, must be zero or positive.")
            raise Exception("Invalid Equity ID, must be zero or positive.")

        # Config ID
        if data["config_id"]==None | data['config_id']<0: 
            valid = not valid
            self.logger.error("Invalid Config ID, must be zero or positive.")
            raise Exception("Invalid Config ID, must be zero or positive.")

        # Setting ID
        if data["setting_id"]==None | data['setting_id']<0: 
            valid = not valid
            self.logger.error("Invalid Setting ID, must be zero or positive.")
            raise Exception("Invalid Setting ID, must be zero or positive.")

        # Date Created
        current_date = dt.now().date()
        date = dt.strptime(data["date_created"], "%Y-%m-%d").date()
        # date = date.strftime("%Y-%m-%d")

        if date > current_date:
            valid = not valid
            self.logger.error("Invalid Date Created, must not exceed present date")
            raise Exception("Invalid Date Created, must not exceed present date")

        # Price
        # Quantity
        # Type
        # Type
        # trade_dt --> what kind of validation to perform
        # Ticker --> make request to alphavantage wrapper to see if data["equity_id"] is real

        return valid
    
    def create_trade(self, data=None) -> int:
        
        # data is not provided --> create data
        if data == None:
            ticker = input("Ticker: ")
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            type = int(input("Type: "))
            user_id = int(input("User ID: "))
            equity_id = int(input("Equity ID: "))
            config_id = int(input("Config ID: "))
            setting_id = int(input("Setting ID: "))
            date_created = dt.now()
            trade_dt = None

            data = {
                "ticker": ticker, "price": price, "quantity": quantity,
                "type": type, "user_id": user_id, "quity_id": equity_id,
                "config_id": config_id, "setting_id": setting_id,
                "date_created": date_created, "trade_dt": trade_dt
            }

            return self.trades.insert_one(data).inserted_id
            

        # Data is provided --> insert
        # # If list --> validate, insert each, return ids list
        # Else --> validate and insert
        else:
            if isinstance(data, list):
                inserted_ids = []
                for trade_data in data:
                    try: self._validate(trade_data)
                    except Exception as e: self.logger.error(str(e))
                    else: 
                        result = self.trades.insert_one(trade_data) # Insert trade_data 
                        inserted_ids.append(result.inserted_id)
                return inserted_ids
            
            else:
                try: self._validate(data)
                except Exception as e: self.logger.error(str(e))
                else: 
                    result = self.trades.insert_one(data) # Insert trade data
                    return result.inserted_id
        return 
    
    # Creates a query given some kind of ID --> reduce redundancy?
    @staticmethod
    def create_query(self)->dict:
        config_id = int(input("Enter Config ID ( > 0):"))
        return {"config_id": config_id}

    def read_trade(self, query: dict={}) -> list:
        # Compose a query to read the current user's info if self._id is set and no query was given
        # If empty query --> create one
        # Add queries with user_id, equity_id, settings_id or indivdually?
        if len(query) == 0:
            query = self.create_query()

        result = list(self.trades.find(query))
        return result

    def update_trade(self, query:dict={}, values: dict={}, many = False) -> int:
        if len(query) <= 0:
            query = self.create_query()

        # No update values --> create values
        if len(values) <= 0:
            values = {}
            print("Leave it blank to skip")

            ticker = input("Ticker: ")
            if ticker!="": values["ticker"] = ticker

            price = float(input("Price: "))
            if price!="": values["price"] = price

            quantity = int(input("Quantity: "))
            if quantity!="": values["quantity"] = quantity

            type = int(input("Type: "))
            if type!="": values["type"] = type

            user_id = int(input("User ID: "))
            if user_id!="": values["user_id"] = user_id

            equity_id = int(input("Equity ID: "))
            if equity_id!="": values["equity_id"] = equity_id

            config_id = int(input("Config ID: "))
            if config_id!="": values["config_id"] = config_id
            
            setting_id = int(input("Setting ID: "))
            if setting_id!="": values["setting_id"] = setting_id

            values = {"$set": values} # Reformat to fit pymongo

        # If many --> update all matching docs
        # Else --> Update one doc
        if many == False: updated = self.trades.update_many(query, values)
        else: updated = self.trades.update_one(query, values)
            
        return updated.modified_count
    
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





    
    