import os
from pymongo import MongoClient
MONGODB_PWD = os.environ.get('MONGODB_PWD')

connection_string = f"mongodb+srv://noy00y:{MONGODB_PWD}@cluster0.yq70vqw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

dbs = client.list_database_names()
