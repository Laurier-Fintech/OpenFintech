from .FinSQL import FinSQL
from datetime import datetime as dt
import pandas as pd
import requests
import numpy as np

# TODO:     
    # Crypto Intraday method (can be pulled from Alphavantage)
    # Handling edge cases (where error occurs when the DB has no data, how to loop and get the data and sucessfully handle the method call)

class FinData: 
    def __init__(self, database=None, key="", keys=[], refresh=30):
        if database==None: database = FinSQL()
        self.db = database
        
        # Setup key/keys
        self.key = key # Is empty if the user provided a list of keys
        self.keys = {key: 0 for key in keys} 
        if len(self.keys)==0 and self.key=="": raise Exception("Please provide an Alphavantage key or a list of Alphavantage keys.")
        if len(self.keys)==0 and self.key!="": self.keys[self.key]=0 # NOTE: From this point on, only self.keys will be used.
        
        self.refresh = refresh # 30 days by default
        return
    
    def overview(self, ticker:str): # NOTE: Currently works for equities only, stores overviews in our DB too 
        key = self.get_key(self.keys)
        result = self.equities.find_one({"ticker": ticker}) # Check if the given ticker exists in the equities collection
        if (result==None) or (result!=None and ((dt.now() - result["date_created"]).days > self.refresh)): # If the data is not available in the equities collection (or if the data is outdated)
            # Request data, create new document, and insert into the DB
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={key}"
            response = self._request(url) # If it fails, loop back
            document = {
                "ticker": response["Symbol"],"date_created": dt.now(),"CIK": response["CIK"],
                "description": response["Description"],"name": response["Name"],
                "country": response["Country"],"currency": response["Currency"],
                "exchange": response["Exchange"], "address": response["Address"],
                "industry": response["Industry"],"sector":response["Sector"]
            }
            self.equities.insert_one(document) # Add the entry to the collection
            result = self.equities.find_one({"ticker": ticker}) # Call find_one again? 
        return result

    def crypto_overview(self, name:str):
        # Check the collection for the data, if available and within x period, send the data
        result = self.crypto.find_one({"ticker": name}) # Check if the given ticker exists in the crypto collection
        if result==None: # If the data is not available in the crypto collection (or if the data is outdated)
            url = f"https://api.coincap.io/v2/assets/{name}"
            response = self._request(url) # If it fails, loop back
            document = {
                "date_created": dt.now(),"symbol": response["symbol"],
                "name": response["name"], "supply": response["supply"],
                "maxSupply": response["maxSupply"], "marketCapUsd": response["marketCapUsd"],
            }
            self.crypto.insert_one(document) # Add the entry to the collection
            result = self.equities.find_one({"ticker": name}) 
        return result

    # Internal utility functions (can be used externally as well as they are esentially independent from the package (no self parm.))
    @staticmethod
    def get_key(keys:dict):
        if len(keys)==0: raise Exception("No keys given.")
        key = min(keys, key=keys.get)
        keys[key]+=1
        return key

    @staticmethod 
    def _request(url:str): 
        # Has error handling for our own request module 
        response = requests.get(url)
        # Check if the request's response is valid/if it failed
        if response.status_code==200: # Check if the request worked 
            try: response = response.json()
            except: 
                raise Exception("Failed to convert response to JSON.")
            else:
                if "Note" not in response.keys(): 
                    return response
                else: 
                    raise Exception("Exceeded request limit")
        raise Exception(f"Request Failed {response.status_code}")
    
    @staticmethod
    def equity_intraday(key:str, ticker:str, start:str="", end:str="", interval:int=5): # Default interval is 5 mins        
        if (start!="" and end=="") or (start=="" and end!=""): raise Exception("Please provide the missing date range value")

        endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&apikey={key}"
        response = FinData._request(endpoint)
        df = pd.DataFrame(response["Time Series (5min)"]).T.reset_index().rename(columns={"index":"0. timestamp"}) # Transpose, reset index, and set index col name as date
        df['0. timestamp'] = pd.to_datetime(df['0. timestamp'])
        if start!="" and end!="": # Convert the start and end dates for the desired date range into a pandas dt and return the filtered df
            start_date = pd.to_datetime(start)
            end_date = pd.to_datetime(end)
            filtered_df = df[(df['0. timestamp'] >= start_date) & (df['0. timestamp'] <= end_date)].reset_index(drop=True)
            df = filtered_df
        return df
    
    @staticmethod
    def lookup(key:str, ticker:str, check=False, full=False):
        if key==None or ticker==None: raise Exception("Please provide a ticker and a key to use the lookup function")
        if check==True and full==True: raise Exception("Please avoid having both check and full set to true simultaneously.")

        endpoint = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={key}"
        response = FinData._request(endpoint)

        if full==False:
            response = [ticker['1. symbol'] for ticker in response['bestMatches']] # Extract tickers from the response
            if check==True: # Set variable to return as a boolean (true if user ticker exists in symbols)
                response = ticker.lower() in [ticker.lower() for ticker in response]

        return response

    @staticmethod
    def technical_indicator(indicators: dict, df: pd.DataFrame):
        for indicator in indicators:
            if indicator == "SMA":
                for param in indicators[indicator]:
                    df[f'{indicator}_{param}'] = df['4. close'].rolling(param).mean()
            elif indicator == "EMA":
                for param in indicators[indicator]:
                    df[f'{indicator}_{param}'] = df["4. close"].ewm(com=param).mean()
            elif indicator == "RSI":
                for param in indicators[indicator]:
                    delta = df["4. close"].astype('float').diff()
                    delta = delta[1:] 
                    
                    up = delta.clip(lower=0)
                    down =  delta.clip(upper=0).abs()
                    
                    roll_up = up.ewm(com=param).mean()
                    roll_down = down.ewm(com=param).mean()

                    rs = roll_up / roll_down
                    rsi = 100.0 - (100.0 / (1.0 + rs))

                    rsi[:] = np.select([roll_down == 0, roll_up == 0, True], [100, 0, rsi])
                    df[f'{indicator}_{param}'] = rsi
            else:
                raise Exception("Please provide a valid indicator, such as SMA, EMA, or RSI.")
        
        return df