import os 
from dotenv import load_dotenv
from OpenFintech import FinMongo, FinData
import pandas as pd

load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS') 
ALPHAVANTAGE_KEY = "XOW4K6WRTDX8S951"

# Need to write new driver code to test with real sequence