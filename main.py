import os 
from dotenv import load_dotenv
from OpenFintech import FinMongo, FinData
import pandas as pd

load_dotenv()
MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASS = os.getenv('MONGO_PASS') 
ALPHAVANTAGE_KEY = "XOW4K6WRTDX8S951"

"""
mycol = mydb["price"] # create collection
sample_data = {
    "2023-06-02": {
        "1. open": "129.5600",
        "2. high": "133.1200",
        "3. low": "127.4600",
        "4. close": "132.4200",
        "5. volume": "24339245"
    },
    "2023-05-26": {
        "1. open": "127.5000",
        "2. high": "129.6600",
        "3. low": "125.0100",
        "4. close": "128.8900",
        "5. volume": "21029979"
    }
}
data = []
for key in sample_data: 
    sample_data[key].update({"0. date": key})
    data.append(sample_data[key])
print(data)
mycol.insert_many(data)

"""


# NOTE: Currently facing one error (no module named pymongo-inmemory). Possible solution is to explictily mention it in setup.py

#finmongo = FinMongo(f"mongodb+srv://{MONGO_USER}:{MONGO_PASS}@cluster0.lvkyalc.mongodb.net/?retryWrites=true&w=majority")     
#findata = FinData(key=ALPHAVANTAGE_KEY,database=finmongo.client["mydatabase"])

df = FinData.equity_intraday(ticker="AAPL",key=ALPHAVANTAGE_KEY)

print(df)

#findata.close()
#finmongo.disconnect()