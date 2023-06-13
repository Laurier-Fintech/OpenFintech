# FinMongo Package Documentation

## Description

The `FinMongo` package is a Python wrapper around the MongoDB database system, providing functionality to connect to either a local in-memory database or an external MongoDB server. The package also provides methods to close the connection and to represent the current instance as a string, which contains server information.

## Dependencies

- `pymongo`
- `pymongo_inmemory`
- `logging`
- `utilities`

## Class Definition

### `FinMongo(host: str = None, logger:logging.Logger = None)`

Initializes a new instance of the `FinMongo` class.

**Parameters**

- `host` (`str`, optional): MongoDB server URI. If not provided, an in-memory database is created.
- `logger` (`logging.Logger`, optional): Logger object. If not provided, a new logger with name "finmongo" is created.

### Methods

#### `connect()`

This method is reserved for switching hosts or handling multiple connections. As of the latest version, it is yet to be built.

#### `disconnect() -> bool`

Closes the current MongoDB client connection.

**Returns**

- `bool`: Returns `True` if the connection was successfully closed, and `False` otherwise.

#### `__str__() -> str`

Returns a string representation of the current instance, containing information about the server. Currently, it returns the MongoDB server info.

**Returns**

- `str`: String representation of the server information.

## Example Usage

Below is a sample usage of the `FinMongo` package:

```python
from dotenv import load_dotenv
import os 

load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS') 
handler = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority")

client = handler.client

mydb = client["mydatabase"]
mycol = mydb["users"]
sample_data = {
    "date_created": None,
    "user_id": 3, "username": "Brown",
    "major":"CS", "year": 30,
    "email": None, "password": None
}

x = mycol.insert_one(sample_data)

print(client.list_database_names())
print(mydb.list_collection_names())
print(x.inserted_id)

handler.disconnect()
```

In the example above, we load the MongoDB credentials from a `.env` file, use them to connect to the MongoDB server, create a new database named `mydatabase`, add a collection named `users` to it, and insert one document into the `users` collection. We then list the database names and collection names, and print the ID of the inserted document. Finally, we disconnect from the MongoDB server.

## Future Work

This package is a work in progress, and there are plans to add the following features:

- A complete `__str__` function implementation to provide more detailed server information.
- CRUD (Create, Read, Update, Delete) operations.
- Custom error messages returned in dict/JSON format, similar to API responses.
- A fully functional `connect()` method for switching hosts or handling multiple connections.

# User Package Documentation

## Description

The `User` package is a Python wrapper for interacting with user data stored in MongoDB. The package provides functionality to create, read, update, and delete user records, which are represented as documents in a MongoDB collection. It is built on top of the `FinMongo` package.

## Dependencies

- `logging`
- `FinMongo`
- `utilities`

## Class Definition

### `User(collection=None, logger:logging.Logger=None)`

Initializes a new instance of the `User` class.

**Parameters**

- `collection` (`pymongo.Collection`, optional): MongoDB collection object where user data will be stored. If not provided, an in-memory MongoDB database and collection named 'users' are created.
- `logger` (`logging.Logger`, optional): Logger object. If not provided, a new logger with name "user" is created.

### Properties

#### `id`

This property is used to get or set the user's ID, and it must be a positive integer.

### Methods

#### `_validate(data: dict) -> bool`

This is an internal method used for validating a user data dictionary.

**Parameters**

- `data` (`dict`): User data to validate.

**Returns**

- `bool`: `True` if the data is valid, and `False` otherwise.

#### `create(data=None) -> int`

Creates a new user document in the MongoDB collection and returns the MongoDB ObjectID of the created document.

**Parameters**

- `data` (`dict` or `list` of `dict`, optional): User data to store. If not provided, user data is requested interactively from the console.

**Returns**

- `int`: The MongoDB ObjectID of the created document.

#### `read(query:dict={}) -> list`

Reads and returns user documents from the MongoDB collection that match the provided query.

**Parameters**

- `query` (`dict`, optional): MongoDB query to select documents. If not provided and the user's ID is set, it reads documents with the user's ID.

**Returns**

- `list`: List of matching documents.

#### `delete(query:dict={}, many=False) -> int`

Deletes user documents from the MongoDB collection that match the provided query.

**Parameters**

- `query` (`dict`, optional): MongoDB query to select documents. If not provided and the user's ID is set, it deletes the document with the user's ID.
- `many` (`bool`, optional): If `True`, deletes all matching documents. If `False`, deletes only the first matching document.

**Returns**

- `int`: The count of deleted documents.

#### `update(query={}, values={}, many=False) -> int`

Updates user documents in the MongoDB collection that match the provided query.

**Parameters**

- `query` (`dict`, optional): MongoDB query to select documents. If not provided and the user's ID is set, it updates the document with the user's ID.
- `values` (`dict`, optional): MongoDB update document. If not provided, update values are requested interactively from the console.
- `many` (`bool`, optional): If `True`, updates all matching documents. If `False`, updates only the first matching document.

**Returns**

- `int`: The count of updated documents.

#### `close()`

Closes the MongoDB connection if it's an in-memory connection.

#### `__str__()`

Returns a string representation of the user. Currently, this method is not implemented.

## Future Work

This package is a work in progress, and there are plans to add the following features:

- Functionality to insert multiple users at once.
- Improved data validation, including email format validation.
- A complete `__str__` method

 implementation to provide a summary of a user profile.
- Use of `self.logger` to add logging statements to the package.

# Market Package Documentation

## Description

The `Market` package is a Python wrapper for interacting with trade and position data stored in MongoDB. The package provides functionalities to create, read, update, and delete both positions and trades, which are represented as documents in a MongoDB collection. 

The `Market` class supports two modes of operation: a real-time mode that operates on open positions, and a backtesting mode that operates on completed trades. It is built on top of the `FinMongo` package.

## Dependencies

- `FinMongo`
- `utilities`

## Class Definition

### `Market(database=None, logger=None)`

Initializes a new instance of the `Market` class.

**Parameters**

- `database` (`pymongo.Database`, optional): MongoDB database object where market data will be stored. If not provided, an in-memory MongoDB database is created.
- `logger` (`logging.Logger`, optional): Logger object. If not provided, a new logger with name "market" is created.

### Methods

Real-time market functionalities:

#### `open_position()`

Opens a new position in the market. This method is not implemented yet.

#### `close_position()`

Closes an open position in the market. This method is not implemented yet.

#### `update_position()`

Updates an open position in the market. This method is not implemented yet.

#### `view_position()`

Retrieves the details of an open position in the market. This method is not implemented yet.

Backtesting functionalities:

#### `create_trade()`

Creates a new trade record for backtesting. This method is not implemented yet.

#### `read_trade()`

Reads a trade record for backtesting. This method is not implemented yet.

#### `update_trade()`

Updates a trade record for backtesting. This method is not implemented yet.

#### `delete_trade()`

Deletes a trade record for backtesting. This method is not implemented yet.

Other methods:

#### `close()`

Closes the MongoDB connection if it's an in-memory connection.

#### `__str__()`

Returns a string representation of the market. Currently, this method is not implemented.

## Future Work

This package is a work in progress, and there are plans to add the following features:

- Create an ERD focusing on the required collections to support test configuration.
- Complete the CRUD functions for positions and trades.
- Integrate `FinData` (Alphavantage Wrapper Package) into the `Market` to get the required Trade and Position Data. The `Market` package should also be able to return this data when requested.
- Implement `__str__` to provide an overview of the market.

# Model Package Documentation

## Description

The `Model` package is a Python package designed to interact with and manipulate trading model configurations and settings. It is built on top of the `FinMongo` and `Market` packages. The package provides functionalities to create, read, update, and delete configurations as well as to perform backtesting and real-time testing of a given configuration.

## Dependencies

- `FinMongo`
- `Market`
- `utilities`

## Class Definition

### `Model(database=None, logger=None)`

Initializes a new instance of the `Model` class.

**Parameters**

- `database` (`pymongo.Database`, optional): MongoDB database object where market data will be stored. If not provided, an in-memory MongoDB database is created.
- `logger` (`logging.Logger`, optional): Logger object. If not provided, a new logger with name "model" is created.

### Methods

#### `create_config()`

Creates and saves a new trading model configuration. This method is not implemented yet.

#### `read_config()`

Reads an existing trading model configuration. This method is not implemented yet.

#### `update_config()`

Updates an existing trading model configuration. This method is not implemented yet.

#### `delete_config()`

Deletes an existing trading model configuration. This method is not implemented yet.

#### `test_config(setting:dict = {}, configuration:dict={}) -> dict`

Performs backtesting of a given configuration using a specified setting. This method is not implemented yet.

#### `run_config()`

Performs real-time testing of a given configuration. This method is not implemented yet.

#### `close()`

Closes the MongoDB connection if it's an in-memory connection.

#### `__str__()`

Returns a string representation of the model.

## Future Work

This package is a work in-progress, and there are plans to add the following features:

- Configuration CRUD functions
- Referential integrity validation where required (possibly create a `_validate` function)
- Implement `test_config` based on the provided notes
- Implement the `__str__` function

## Examples

The following example demonstrates how to create an instance of the `Model` class and print it:

```python
model = Model()
print(model)
model.close()
```