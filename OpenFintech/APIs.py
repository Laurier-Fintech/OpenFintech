from .Databases import MySQL
from . import queries
import requests
import pandas as pd
import numpy as np
from datetime import datetime as dt

# TODO:     
    # Ensure overview is returning the last entry to equity for a given ticker (else update the query in queries.py)
    # Handling edge cases (where error occurs when the DB has no data and API fails ??)

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
                self.db_handler.execute(queries.insert_equity_complete, values=
                    (
                        response["Symbol"],
                        response["Name"],response["Description"],response["CIK"],
                        response["Country"],response["Currency"],response["Exchange"],
                        response["Address"],response["Industry"],response["Sector"],
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
    def equity_intraday(key:str, ticker:str, start:str="", end:str="", interval:int=5): # Default interval is 5 mins        
        if (start!="" and end=="") or (start=="" and end!=""): raise Exception("Please provide the missing date range value")
        endpoint = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&apikey={key}"
        response = Alphavantage._request(endpoint)
        df = pd.DataFrame(response["Time Series (5min)"]).T.reset_index().rename(columns={"index":"0. timestamp"}) # Transpose, reset index, and set index col name as date
        df['0. timestamp'] = pd.to_datetime(df['0. timestamp'])
        if start!="" and end!="": # Convert the start and end dates for the desired date range into a pandas dt and return the filtered df
            start_date = pd.to_datetime(start)
            end_date = pd.to_datetime(end)
            filtered_df = df[(df['0. timestamp'] >= start_date) & (df['0. timestamp'] <= end_date)].reset_index(drop=True)
            df = filtered_df
        return df
    
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

if __name__=="__main__":
    import queries
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    SQL_USER = os.getenv('MYSQL_USER')
    SQL_PASS = os.getenv('MYSQL_PASS') 
    host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
    handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    key="NDYBGSF1PGZROO4Q"
    data = Alphavantage(handler, key="NDYBGSF1PGZROO4Q")
    result = data.overview("META")
    print(result)
    handler.disconnect()

    raw_df = data.equity_intraday(key=key, ticker="META")
    print(raw_df)

    indicators = {
        "RSI": [10,5],
        "EMA": [10,5],
        "SMA": [10,5],
    }
    df_with_indicator = data.technical_indicator(indicators=indicators,df=raw_df)
    print(df_with_indicator)
    