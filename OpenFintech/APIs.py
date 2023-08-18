from .Databases import MySQL
from . import queries
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt

# TODO: Handling edge cases (where error occurs when the DB has no data and API fails ??)

class Alphavantage: 
    def __init__(self, database:MySQL, key="", keys=[], refresh=30):
        self.db_handler = database
    
        # Setup key/keys
        self.key = key # Is empty if the user provided a list of keys
        self.keys = {key: 0 for key in keys} 
        if len(self.keys)==0 and self.key=="": raise Exception("Please provide an Alphavantage key or a list of Alphavantage keys.")
        if len(self.keys)==0 and self.key!="": self.keys[self.key]=0 # NOTE: From this point on, only self.keys will be used.
        
        self.refresh = refresh # 30 days by default
        return
    
    def overview(self, ticker:str): # NOTE: Currently works for equities only, stores overviews in our DB to reduce key usage 
        
        result = self.db_handler.execute(queries.select_ticker_entry, values=(ticker,), query=True) # Check if the given ticker exists in the equities table        
        
        if (isinstance(result, list)==True):
            if (len(result)==0 or ((dt.now() - result[0][2]).days > self.refresh)): # If the data is not available in the equities table (or if the data is outdated)
                # Request data from Alphavantage API, create new entry, and insert into the DB
                url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={self.get_key(self.keys)}"
                response = self._request(url)
                try:
                    self.db_handler.execute(queries.insert_equity_complete, values=
                        (
                            response["Symbol"],
                            response["Name"],response["Description"],response["CIK"],
                            response["Country"],response["Currency"],response["Exchange"],
                            response["Address"],response["Industry"],response["Sector"],
                        )
                    )
                except:
                    self.db_handler.execute(queries.insert_equity_short, values=
                        (
                            ticker,
                        )
                    )
                result = self.db_handler.execute(queries.select_ticker_entry, values=(ticker,), query=True)[0]
            else: result = result[0] # If no refresh is required, grab the latest one to return

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
    def lookup(key:str, ticker:str, check=False, full=False): # Returns either the list of tickers, boolean if given ticker exists, or the full response as is
        if key==None or ticker==None: raise Exception("Please provide a ticker and a key to use the lookup function")
        if check==True and full==True: raise Exception("Please avoid having both check and full set to true simultaneously.")

        endpoint = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={key}"
        response = Alphavantage._request(endpoint)

        if full==False:
            response = [ticker['1. symbol'] for ticker in response['bestMatches']] # Extract tickers from the response
            if check==True: # Set variable to return as a boolean (true if user ticker exists in symbols)
                response = ticker.lower() in [ticker.lower() for ticker in response]

        return response

    @staticmethod
    def equity_daily(key:str, ticker:str):
        response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={key}")
        response = response["Time Series (Daily)"]
        df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]
        return df

    @staticmethod
    def equity_intraday(key:str, ticker:str, interval:int=5): # Default interval is 5 mins        
        response = Alphavantage._request(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&apikey={key}")
        response = response[f"Time Series ({interval}min)"]
        df = pd.DataFrame.from_dict(response, orient="index", dtype=float).iloc[::-1]
        return df
    
    @staticmethod
    def technical_indicator(indicators: dict, df: pd.DataFrame):
        i = len(df.columns) + 1
        for indicator in indicators:
            if "EMA" in indicator:
                df[f'{i}. {indicator}'] = df["4. close"].ewm(span=int(indicator[3:]), adjust=False).mean()
            elif "SMA" in indicator:
                df[f'{i}. {indicator}'] = df["4. close"].rolling(window=int(indicator[3:])).mean()
            i+=1
        df.dropna(inplace=True)
        return df