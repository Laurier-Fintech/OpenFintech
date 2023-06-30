import logging
from datetime import datetime as dt
from .FinMongo import FinMongo
from .utilities import create_logger
# TODO:
# Add functionality to insert many users (data in create_users could be a list of dict's)
# Improve data validation (e.x., email format validation) 

class User:
    def __init__(self, collection=None, logger:logging.Logger=None): 

        # Setting logger
        if logger==None: logger = create_logger("user")
        self.logger = logger

        self.inmemory = False
        # General Attributes:
        if collection==None: # When no collection is given, create a mongoDB and the required 'users' collection
            self.mongo = FinMongo()
            self.inmemory = True
            self.database = self.mongo.client['db']
            self.collection = self.database['users']
        else: self.collection = collection

        # User Specific Attributes/Properties:
        self._id = None # This is get/set using getter/setter methods
        return

    @property 
    def id(self): # NOTE: ID Getter
        return self._id
    
    @id.setter
    def id(self, value:int): # NOTE: ID Setter (to switch ID's and run queries?)
        if value<0: raise Exception("Invalid ID. ID should be > 0")
        self._id = value
        return

    def _validate(self, data: dict) -> bool: # Internal function used for validating a data dictionary 
        valid = True
        if data['user_id']<0: 
            valid = not valid
            self.logger.error("Invalid User ID, must be zero or positive.")
            raise Exception("Invalid User ID, must be zero or positive.")
        if data['username']==None or data['username']=="": 
            valid = not valid
            self.logger.error("Username cannot be empty or none.")
            raise Exception("Username cannot be empty or none.")
        return valid

    # User(s) CRUD functions
    def create(self, data=None) -> int: # This functoin creates a user document and then returns the document ID(s) to the user 
        
        if data==None: # If no data was given, use input statements to get the required information from the user
            
            # Get inputs from user
            user_id = int(input("User ID: "))
            if user_id<0:
                self.logger.error("Invalid User ID, must be zero or positive.")
                raise Exception("Invalid User ID, must be zero or positive.")
            username = input("Username: ")
            if username=="" or username==None: 
                self.logger.error("Usename cannot be empty or none.")
                raise Exception("Usename cannot be empty or none.")
            major = input("Major: ")
            year = int(input("Year: "))
            
            # Pack inputs into a dictionary (i.e., document to add to the collection)
            data = {
                "date_created": dt.now(),
                "user_id": user_id, "username": username,
                "major":major, "year": year,
            }

        else: 
            # For validating multiple documents (given in a list)
            if isinstance(data, list): 
                for user_data in data:
                    print(user_data)
                    try: self._validate(user_data) # Validates data and raises exceptions     
                    except Exception as e: print(e)
                    else: pass 
            # For validating one document (given as a dict)
            else: self._validate(data) 
            
        return self.collection.insert_one(data).inserted_id
    
    def read(self, query:dict={}) -> list: # Get all the records for this ID, return the JSON's (optionally print and return Pandas DF)
        # Compose a query to read the current user's info if self._id is set and no query was given
        if len(query)==0 and self._id!=None: query = {"user_id": self._id}
        result = list(self.collection.find(query))
        return result

    def delete(self, query:dict={}, many=False) -> int:
        # Set query
        if len(query)<=0:
            if self._id!=None: query = {"user_id": self._id}
            else: 
                self.logger.error("No deletion condition, please provide a query for deleting or set the user_id.")
                raise Exception("No deletion condition, please provide a query for deleting or set the user_id.")
        # Call appropriate pymongo delete function
        if many==False: deleted = self.collection.delete_one(query)
        else: deleted = self.collection.delete_many(query)
        return deleted.deleted_count
    
    def update(self, query={}, values={}, many=False) -> int:
        # Set/Get query and values for updating
        if len(query)<=0:
            if self._id==None: raise Exception("To call user.update without query or values, user._id needs to be set using the setter function.")
            query = {"user_id": self._id}

        if len(values)<=0:
            values = {}
            # Get update values from the user
            print("Leave it blank to skip ")
            username = input("Username: ")
            if username!="": values["username"] = username
            major = input("Major: ")
            if major !="": values["major"] = major
            year = input("Year: ")
            if year!="": values["year"] = int(year)
            email = input("Email: ")
            if email!="": values["email"] = email 
            password = input("Password: ")
            if password!="": values["password"] = password
            values = {"$set": values} # Reformat to fit pymongo
            
        # Call appropriate pymongo update function
        if many==False: updated = self.collection.update_many(query, values)
        else: updated = self.collection.update_one(query, values)
        
        return updated.modified_count
    
    def close(self):
        if self.inmemory==True:self.mongo.disconnect()
        return

    def __str__(self):
        data = self.read(self.id)
        str = 'User ID: {}\n'.format(data['user_id']) + 'Username: {}\n'.format(data['username']) + 'Date Created: {}\n'.format(data['date_created']) + 'Major: {}\n'.format(data['major']) + 'Year: {}\n'.format(data['year']) + 'Email: {}\n'.format(data['email'])
        return str

if __name__=='__main__':
    import os 
    from dotenv import load_dotenv
    # Load ENV Variables
    load_dotenv()
    MONGO_USER = os.getenv('MONGO_USER')
    MONGO_PASS = os.getenv('MONGO_PASS') 
    # Setup MongoDB Handler
    db_handler = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority") #TODO: Add ENV var handling functionality    
    #db_handler = FinMongo() # in-memory
    # Connect to DB and Collection
    client = db_handler.client
    database = client["mydatabase"]
    collection = database["users"]
    # Initialize an instance of User with the appropriate collection
    user_handler = User(collection) 
    # Initialize the required sample data
    sample_data = {
        "date_created": None,
        "user_id": 0, "username": "Harri",
        # For analytical purposes
        "major":"CS", "year": 3,
        "email": None, "password": None
    }
    # Add sample_data to user (can also handle creating multiple users)
    # user_handler.create(sample_data)
    user_handler.id = 0
    user_handler.update()

    print(user_handler.read())

    # Disconnect the MongoDB handler
    #user_handler.mongo.disconnect() # For in-memory
    db_handler.disconnect()