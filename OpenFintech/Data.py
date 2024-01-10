from collections import deque 
from typing import Deque
import json

import pandas as pd
import requests

class Candle:
    def __init__(self, open: float, high: float, low: float, close: float, volume: int, datetime: str, durationSeconds: float):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.datetime = datetime
        self.duration_seconds = durationSeconds

class CandleContainer:
    def __init__(self):
        self.candleList: Deque[Candle] = deque()

    def count(self) -> int:
        return len(self.candleList)
    
    def __getitem__(self, index: int) -> Candle:
        return self.candleList[index]

    def front(self) -> Candle:
        if not self.candleList:
            raise IndexError("The CandleContainer is empty.")
        return self.candleList[0]

    def back(self) -> Candle:
        if not self.candleList:
            raise IndexError("The CandleContainer is empty.")
        return self.candleList[-1]

    def pushFront(self, candle: Candle):
        self.candleList.appendleft(candle)

    def pushBack(self, candle: Candle):
        self.candleList.append(candle)

    def popFront(self) -> Candle:
        if not self.candleList:
            raise IndexError("The CandleContainer is empty.")
        return self.candleList.popleft()

    def popBack(self) -> Candle:
        if not self.candleList:
            raise IndexError("The CandleContainer is empty.")
        return self.candleList.pop()

    def clear(self):
        self.candleList.clear()
        
# NOTE: The data structures below are i.e. a replacement to having the database
    
class FinancialInstrument:
    def __init__(self, ticker: str, candle_container: CandleContainer):
        self.ticker = ticker
        self.candle_container = candle_container
        return

# NOTE: The class below was previously a static method within the Alphavantage API wrapper
class Indicator:
    def __init__(self, candle_container: CandleContainer, open_or_close = 'open'):
        self.candle_container = candle_container
        self.open_or_close = open_or_close
        self.indicators = []
        return
    
    def runCalcOnCandleContainer(self):
        return
    
    def returnIndicators(self):
        return self.indicators

class BollingerBands(Indicator):
    def __init__(self, candle_container: CandleContainer, nCandles = 20, open_or_close = 'open'):
        super().__init__(candle_container, open_or_close)


        self.sma = SMA(self.candle_container, self.nCandles, self.open_or_close).indicators[-1] # want a 20-day moving average - may need to adjust # of candles depending on candle frequency
        
        self.nCandles = nCandles

    def runCalcOnCandleContainer(self):

        self.df = pd.DataFrame({'open_price' : candle.open, 'close_price' : candle.close} for candle in self.candle_container.candleList)
        sd = self.df.std()[f'{self.open_or_close}_price']

        upper_band = self.sma + 2*sd
        middle_band = self.sma
        lower_band = self.sma - 2*sd

        self.indicators = [upper_band, middle_band, lower_band]

class NormalizedPrices(Indicator):
    def __init__(self, candle_container: CandleContainer, nCandles, open_or_close = 'open'):
        super().__init__(candle_container, open_or_close)

        self.df = pd.DataFrame({'open_price' : candle.open, 'close_price' : candle.close} for candle in candle_container.candleList)

        self.nCandles = nCandles

    def runCalcOnCandleContainer(self):
        dfcol = self.df[f'{self.open_or_close}_price']
        mean = dfcol.mean()
        sd = dfcol.std()
        normalizedCol = (dfcol - mean)/sd
        self.indicators = normalizedCol.to_list()
        

class SMA(Indicator):
    def __init__(self, candle_container: CandleContainer, nCandles: int, open_or_close = 'open'):
        super().__init__(candle_container, open_or_close)
        
        self.nCandles = nCandles

    def runCalcOnCandleContainer(self):
        self.df = pd.DataFrame({'open_price' : candle.open, 'close_price' : candle.close} for candle in self.candle_container.candleList)
        self.indicators = self.df.rolling(self.nCandles).mean()[f'{self.open_or_close}_price'].to_list()


# NOTE: This class was previously a part of the API wrapper
class DataAcquisition: 
    def __init__(self, key: str):
        self.key = key
        return
    
    def _request(): # Could use an internal request method that simplifies things (check out the old Alphavantage wrapper code)
        return

    def requestDataFromAPI(self, ticker, interval, outputsize='full'): # declare return type, parameters should be for our functionality
        params = None

        if interval == 'daily':
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': ticker,
                'outputsize': 'compact',
                'apikey': self.key,
            }
        else:
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': ticker,
                'interval': f'{interval}min', # '1min', '5min', '15min', '30min', '60min
                'outputsize': outputsize,
                'apikey': self.key,
            }
        
        response = requests.get(url="https://www.alphavantage.co/query", params=params)
        response.raise_for_status()
        return response.json()
    
    def convertDataToFinancialInstrument(self, jsonDictFromAPI) -> FinancialInstrument:
        candleContainer = CandleContainer()
        
        # Items need to be pushed in reverse order since the API returns the most recent data first
        for key, value in jsonDictFromAPI['Time Series (Daily)'].items():
            candleContainer.pushFront(Candle(
                open = float(value['1. open']),
                high = float(value['2. high']),
                low = float(value['3. low']),
                close = float(value['4. close']),
                volume = int(value['5. volume']),
                datetime = key,
                durationSeconds = 86400
            ))
        return FinancialInstrument(jsonDictFromAPI['Meta Data']['2. Symbol'], candleContainer)