from OpenFintech import *

d = DataAcquisition("6HZIS76ZQIS16EIG")
f = d.requestDataFromAPI('AAPL', 'daily')
# print(f)
# print(f['Time Series (Daily)'].items())
# print("------------------------------------------------------------")
# print(dict(list(reversed(f['Time Series (Daily)'].items()))))
j = d.convertDataToFinancialInstrument(f)
# print symbol, then candle data line by line
for candle in j.candle_container.candleList:
    print(candle.open)
    # print(candle.close)
    # print(candle.high)
    # print(candle.low)
    # print(candle.volume)

sm = SMA(j.candle_container, 5)
sm.runCalcOnCandleContainer()
print(sm.indicators)
