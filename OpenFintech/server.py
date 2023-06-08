import os
from pymongo import MongoClient
MONGODB_PWD = os.environ.get('MONGODB_PWD')

connection_string = f"mongodb+srv://OpenFintech:yT6KHkhVcvHQ42AX@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

dbs = client.list_database_names()
print(dbs)