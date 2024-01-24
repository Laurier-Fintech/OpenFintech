from OpenFintech import *

# Example of how to use the OpenFintech library

# Initialize the API wrapper
apiKey = "6HZIS76ZQIS16EIG"
data_acq = DataAcquisition(apiKey)

# Request data from the API
ticker_symbol = 'AAPL'
timeframe = 'daily' # options: 'daily' or {time}min, e.g. '1min', '5min', '15min', '30min', '60min
tickerData = data_acq.requestDataFromAPI(ticker_symbol, timeframe)

# Convert the data to a FinancialInstrument
ticker_finInst = data_acq.convertDataToFinancialInstrument(tickerData)

# Run calculations on the FinancialInstrument
shortMA = EMA(candle_container = ticker_finInst.candle_container, periodLength = 5)
longMA = SMA(candle_container = ticker_finInst.candle_container, periodLength = 10)

shortMA.runCalcOnCandleContainer()
longMA.runCalcOnCandleContainer()

# Run an algorithm on the FinancialInstrument
tr_algo = TrendFollowing()
tr_backtest_data = tr_algo.runAlgorithmOnCandleContainer(
                                    candle_container = ticker_finInst.candle_container,
                                    short_ma = shortMA,
                                    long_ma = longMA,
                                    stop_loss = 0.05,
                                    take_profit = 0.1,
                                    assets = 10000
                                    )

print(tr_backtest_data)

mr_algo = MeanReversion()
mr_backtest_data = mr_algo.runAlgorithmOnCandleContainer(
                                    candle_container = ticker_finInst.candle_container,
                                    short_ma = shortMA,
                                    long_ma = longMA,
                                    stop_loss = 0.05,
                                    take_profit = 0.1,
                                    assets = 10000
                                    )

print(mr_backtest_data)