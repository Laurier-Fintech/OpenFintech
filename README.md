# OpenFintech

## Introduction
OpenFintech is a financial analysis library designed for Python developers and financial analysts. It provides powerful tools for conducting both trend following and mean reversion analyses, utilizing financial market data. This project aims to make complex financial algorithms accessible and easy to use.

## Installation
To install OpenFintech, follow these steps:

1. Ensure you have Python installed on your system.
2. Clone the repository:
   ```bash
   git clone https://github.com/your-username/OpenFintech.git
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Here's a quick example of how to use OpenFintech to run financial algorithms:

```python
from OpenFintech import *

# Initialize and get data
data_acq = DataAcquisition("your-api-key")
tickerData = data_acq.requestDataFromAPI('AAPL', 'daily')

# Convert to FinancialInstrument
ticker_finInst = data_acq.convertDataToFinancialInstrument(tickerData)

# Run algorithms
tr_algo = TrendFollowing()
tr_backtest_data = tr_algo.runAlgorithmOnCandleContainer(...)
mr_algo = MeanReversion()
mr_backtest_data = mr_algo.runAlgorithmOnCandleContainer(...)

print(tr_backtest_data)
print(mr_backtest_data)
```

Replace `"your-api-key"` with your actual API key.

## Components
### Model.py
- `Algorithm`: Base class for trading algorithms.
- `MeanReversion`: Implements the mean reversion strategy.
- `TrendFollowing`: Implements the trend following strategy.

### Data.py
- `Candle`, `CandleContainer`: Represent market data.
- `FinancialInstrument`: Represents a financial instrument with associated market data.
- `Indicator`, `BollingerBands`, `NormalizedPrices`, `SMA`: Various financial indicators.
- `DataAcquisition`: Handles data acquisition from external sources.

## Contributing
Contributions are welcome! Please read our contributing guidelines to get started.

## License
This project is licensed under the Apache License - see the LICENSE file for details.

## FAQs/Contact Information
For any queries, please reach out to us at team@wlufintech.com.