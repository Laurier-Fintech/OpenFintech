import logging
import pymongo_inmemory
from pymongo import MongoClient, errors
from .utilities import create_logger
# TODO: 
# Add static function that, given a collection, returns the last record that was entered into it (carrying any other filter as given)

class FinMongo:

    def __init__(self, host: str = None, logger:logging.Logger = None):

        if logger==None: logger = create_logger("finmongo")
        self.logger=logger
                
        if host==None:
            # If no host connection str was given, create and return an in-memory database
            self.client = pymongo_inmemory.MongoClient()
            self.logger.info("Successfully created a in-memory MongoDB.")
        else:
            # Establish connection with mongo cluster
            try:
                self.client = MongoClient(host) # host connection string
                self.client.server_info()  # force connection request for testing 
            except errors.ConnectionFailure:
                self.logger.exception("Could not connect to MongoDB (Error: Connection Failure).")   
            else: 
                self.logger.info("Successfully connected to MongoDB.")
            
        return

    def connect(self):
        # This function would be built to switch hosts or handle multiple connections
        return

    def disconnect(self):
        success = False
        if self.client: 
            try: self.client.close()
            except: self.logger.error("Failed to close the connection.")
            else: 
                self.logger.info("Sucessfully closed the connection.")
                success = True
        return success

    def __str__(self): # Print the status (connection overview) and other information
        databases = self.client.list_database_names() # databases in cluster
        database_info = []
        for db_name in databases:
            db_info = {
                'database': db_name,
                'collections': []
            }
            db = self.client[db_name]
            collections = db.list_collection_names()
            for c_name in collections:
                collection = db[c_name]
                docs = collection.count_documents({})
                c_info = {
                    'collection': c_name,
                    'doc_count': docs
                }
                db_info["collections"].append(c_info)
            database_info.append(db_info)
        return str(database_info)