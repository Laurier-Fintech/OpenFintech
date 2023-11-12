from collections import deque 
from typing import Deque

class Candle:
    def __init__(self, open_price: float, high: float, low: float, close_price: float, volume: int, datetime: str, durationSeconds: float):
        self.open_price = open_price
        self.high = high
        self.low = low
        self.close_price = close_price
        self.volume = volume
        self.datetime = datetime
        self.duration_seconds = duration_seconds

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
    def __init__(self):
        return

# NOTE: The class below was previously a static method within the Alphavantage API wrapper
class Indicator:
    def __init__(self):
        return

# NOTE: This class was previously a part of the API wrapper
class DataAcquisition: 
    def __init__(self):
        return
    
    def _request(): # Could use an internal request method that simplifies things (check out the old Alphavantage wrapper code)
        return

    def requestDataFromAPI(self, ticker, interval, outputsize='full'): # declare return type, parameters should be for our functionality
        params = {
            'function': 'TIMESERIES' + interval.upper(),
            'symbol': ticker,
            'apikey': self.key,
            'outputsize': outputsize
        }
        response = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval={interval}min&apikey={self.key}", params=params)
        response.raise_for_status()
        return response.json()
    
    def convertDataToCandleContainer(self): # return type is a candle container
        return