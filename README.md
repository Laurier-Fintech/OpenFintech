# **📦 OpenFintech: Opensource Fintech Library**

### **1. Introduction**

OpenFintech is a pioneering project designed with the primary objective of allowing users to create custom high-frequency trading algorithms and introducting them to financial technology as a field 💻. This project also includes wrappers for MySQL, MongoDB (in-development), and Alphavantage (a financial information API)*.*

#### **1.1. Who Is OpenFintech For?**

OpenFintech is tailored for:

- **Students** who have a keen interest in:
  - Delving deeper into trading algorithms.
  - Grasping the basics of algorithmic trading and fintech.
  - Undertaking both backtesting and simulated live testing of their algorithmic trading strategy.

---

### **2. The Heart of OpenFintech: Mean Reversion Strategy**

#### **2.1. Conceptualizing Mean Reversion**

Mean reversion is the cornerstone of the strategies offered by OpenFintech. It is premised on the theory that asset prices, volatility, and historical returns will eventually revert to the long-run mean of the entire dataset. In the financial realm, this mean can manifest in various contexts, such as a stock's historical price data, P/E ratio or the average return of an industry sector.

#### **2.2. Potential Risks**

It's crucial to note that a return to the norm isn't always guaranteed. Unexpected market highs or lows could signal a shift in the usual trend. Events that might trigger such shifts include product launches or, on the flip side, recalls and lawsuits.

---

### **3. The Brain Behind the Operations: Model.py and Backtesting**

At the core of OpenFintech's algorithmic strategies is the `Model.py` file, which focuses on backtesting the strategies to provide users with realistic and insightful simulations.

#### **3.1. Algorithmic Trading Strategies our system offers (for now at least 👀)**

1. Moving Average (SMA) with Different Periods:
   - In this strategy, the system considers two distinct moving averages: one short-term (like the 50-day moving average) and one long-term (like the 200-day moving average).
   - Long Signal: When the short-term moving average crosses above the long-term moving average, this is a potential sign that the asset is in an upward momentum, thus generating a buy (or "long") signal.
   - Short Signal: Conversely, when the short-term moving average crosses below the long-term moving average, the asset might be experiencing a downturn, thus generating a sell (or "short") signal.
   - Customizable parameters:
     - Moving averages (e.x. SMA and EMA) and their associated periods

---

### **4. How To Use**

Here's a step-by-step guide to using the OpenFintech package:

1. **Installation**:
   Begin by installing the OpenFintech package using pip.

   ```bash
   pip install OpenFintech
   ```
2. **Setting Up The File**:
   After installation, create a Python script and import the required classes from the OpenFintech package.

   ```python
   from OpenFintech import MySQL, Alphavantage, Model, User
   ```
3. **Variable Configuration**:
   Before proceeding, set up the necessary variables for your database and API configurations. It's recommended to use environment variables to store these values securely.

   ```python
   SQL_USER, SQL_PASS, ALPHAVANTAGE_KEY = "username", "password", "apikey"
   host = "hosturl"
   ```
4. **Initialization**:
   With the above variables, initiate the various handlers:

   - Database handler for MySQL
   - User handler
   - API handler for Alphavantage
   - Model handler

   ```python
   db_handler = MySQL(host=host, user=SQL_USER, password=SQL_PASS, database="main")
   user_handler = User(database=db_handler)
   api_handler = Alphavantage(database=db_handler, key=ALPHAVANTAGE_KEY)
   model_handler = Model(database=db_handler)
   ```
5. **User Creation**:
   Use the `create` method from the `user_handler` to create a new user and retrieve their ID.

   ```python
   user_id = user_handler.create(values=("Harri",), simple=True)
   ```
6. **Setting Backtesting Parameters**:
   Define a dictionary for backtesting settings. This dictionary will contain parameters like starting amount, short and long strategies, stock ticker, and more.

   ```python
   setting_values = {
       "user_id": user_id,
       "starting_aum": 100000,
       "short": "EMA 5",
       "long": "SMA 15",
       "ticker": "NIO",
       "stop_loss": 10, #%
       "take_profit": 0.5,#%
       "chart_freq_mins": 0
   }
   ```
7. **Fetching Price Data**:
   With the settings in place, fetch the daily equity data for the given ticker using the Alphavantage package.

   ```python
   df = api_handler.equity_daily(key=Alphavantage.get_key(api_handler.keys), ticker=setting_values["ticker"])
   ```
8. **Applying Technical Indicators**:
   Based on your backtesting settings, apply the relevant technical indicators to the fetched data.

   ```python
   indicators = [''.join(setting_values["short"].split(" ")), ''.join(setting_values["long"].split(" "))]
   df = api_handler.technical_indicator(indicators, df)
   ```
9. **Backtesting**:
   Call the backtest function from the model handler with the previously defined settings and the modified price data.

   ```python
   response = model_handler.backtest(setting_values, df)
   print(response)
   ```
10. **Clean Up**:
    After completing all operations, make sure to close the connection to the database.

```python
   db_handler.disconnect()
   print("Disconnected database connection.")
```

Note: Always ensure that sensitive data such as passwords and API keys are stored securely and are not hard-coded directly into the script.

---

### **5. Output**

The output of Model.backtest contains the price data as a pandas df and the performance of the settings provided to the algorithm.

- {'price_data':             1. open  2. high    3. low  4. close    5. volume     6. EMA5    7. SMA15
  2023-04-18  187.150   187.69  183.5775    184.31   92067016.0  185.355453  189.188667
  2023-04-19  179.100   183.50  177.6500    180.59  125732687.0  183.766969  188.615333
  2023-04-20  166.165   169.70  160.5600    162.99  210970819.0  176.841313  186.556000
  2023-04-21  164.800   166.00  161.3208    165.08  123538954.0  172.920875  184.542667
  2023-04-24  164.650   165.65  158.6100    162.55  140006559.0  169.463917  181.548667
  ...             ...      ...       ...       ...          ...         ...         ...
  2023-08-14  235.700   240.66  233.7500    239.76   98595331.0  244.249615  254.577333
  2023-08-15  238.730   240.50  232.6100    232.96   88197599.0  240.486410  252.422667
  2023-08-16  228.020   233.97  225.3800    225.60  112484520.0  235.524273  249.839333
  2023-08-17  226.060   226.74  218.8300    219.22  120718417.0  230.089516  247.406667
  2023-08-18  214.120   217.58  212.3600    215.49  136276584.0  225.223010  244.010000 
- [86 rows x 7 columns], 'ending_aum': 152490.91942089135, 'dollar_change': 52490.919420891354, 'percent_change': 52.49091942089136}

---

### **6. Conclusion**

OpenFintech, with its emphasis on the mean reversion strategy, provides an unparalleled platform for budding financial analysts and enthusiasts to test, refine, and understand the nuances of algorithmic trading. Whether you're a student or an expert, OpenFintech's extensive features ensure that you're equipped with the tools needed to delve deep into the world of algorithmic trading.

---
