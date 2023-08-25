from .Databases import SQLite3
from . import Alphavantage
from . import queries
import pandas as pd

# TODO: Develop the __str__ function

class Model:
    def __init__(self, database=':memory:'):
        self.handler = SQLite3(name=database)
        for statement in [queries.user_tbl_create, queries.settings_tbl_create, queries.trades_tbl_create, queries.performance_tbl_create]: self.handler.execute(statement)
        self.handler.execute(queries.create_user, values={
            'username': 'Test',
            'email': None,
            'password': None,
            'year': None,
            'major': None
        })
        return
    
    def create(self,values:dict): # Function used to create a settings entry
        lastrowid = self.handler.execute(queries.create_setting, values=values)
        return lastrowid

    def order(self, values:dict): # NOTE: Can add aditional features later on
        lastrowid = self.handler.execute(queries.create_trade, values=values)
        if values["type"]==0: print(f"(#{lastrowid})",values["trade_dt"], ": Buy @", values["price"])
        else: print(f"(#{lastrowid})",values["trade_dt"], ": Sell @", values["price"])
        return lastrowid

    def backtest(self, setting_values:dict, ALPHAVANTAGE_KEY) -> dict:
        print("\nModel.backtest():")

        # Enter the settings into the database
        setting_id = self.create(setting_values)
        print(f"\tCreated setting with the ID {setting_id}")

        # Get additional required info from settings
        aum = float(setting_values["starting_aum"])
        stop_loss = float(setting_values["stop_loss"])
        take_profit = float(setting_values["take_profit"])
        indicators = [''.join(setting_values["short"].split(" ")),''.join(setting_values["long_"].split(" "))]
        # Get the price data for the setting values using the OpenFintech Alphvantage Package
        df = Alphavantage.equity_daily(key=ALPHAVANTAGE_KEY,ticker=setting_values["ticker"])
        # Modify the price_data_df based on the given config values indicators section
        df = Alphavantage.technical_indicator(indicators,df) # Add the tehcnical indicators data to the dataframe
        # Import the data for given the setting using the given api_handler (Alphavantage object)
        print("\tPrice Data + Indicator Data:")
        print(df)

        # Intiailize variables to store temp values to help the algorithm perform calculations
        open = False 
        quantity, purchase_price, sale_price = 0, 0, 0
        
        # Setup variables for the trade history df
        trade_data = []


        # Iterate over the data frame and perform the checks
        for i, r in df.iterrows(): # TODO: CRUD to the trades table
            # Get data from the current row (unit of time)
            date, close, short, long = i, r["4. close"], r[f"6. {indicators[0]}"], r[f"7. {indicators[1]}"]

            if open==False: # At the current unit of time, if there are no open positions....

                if short>long: # Check if the short term mean (base) has passed the long term mean (upper), indicating a upwards change in the price action and a buy signal
                    purchase_price = close # store the purchase price in a variable initialized outside the loop (for referencing in future iterations)
                    quantity = aum / purchase_price # Calculate the maximum purchaseable shares (NOTE: This is a limitation of the current system by design)
                    total = purchase_price * quantity # Calculate the total cost of the purchase 
                    aum -= total # remove cost from balance (NOTE: leaving formula in although this would always be zero due to the limitation highlighted above)
                    
                    # Create buy trade entry
                    data = {"setting_id": setting_id, "type": 0, "trade_dt": i, 
                              "price": purchase_price, "quantity":quantity, "total": total}
                    trade_data.append(data)
                    self.order(data)
                    
                    open = True # Update variable to indicate that a purchase has been made, i.e. position opened.

            else: # When there is an open position.... 
                
                sell = False #NOTE: This boolean variable is used as a trigger to avoid creating a sell function and to avoid writing redundant code

                if short<long: sell = True # If the short term mean has fell underneath the long term mean, indicating a downwards change in the price action, triger the sale of all open positions (NOTE: "all" due to the limitation of the system as discussed earlier)

                else: # When holding, check if the current price, relative to the purchase price, triggers a stop loss or take profit
                    if (close <= (purchase_price - (purchase_price*stop_loss))): sell = True # Conditional statement for stopping loss
                    if (close >= (purchase_price + (purchase_price*take_profit))): sell = True # Conditional statement for taking profit

                if sell: # Code to sell open positions/current holdings (transaction)
                    sale_price = close
                    total = quantity * sale_price # Get the total gained from the sale
                    quantity = 0 # Update the quantity NOTE: Since this is our hypothetical market, when we sell, we assume we find a perfect buyer for all the shares we own at the closing price
                    aum += total # add the total gained from the sale to the aum 
                    # Differentitate between sales that lead to profits vs losses and handle each case differently (NOTE: Potential room for a future project)
                    profitable = False if sale_price<purchase_price else True
                    
                    # Create sale trade entry
                    data = {"setting_id": setting_id, "type": 1, "trade_dt": i, 
                              "price": purchase_price, "quantity":quantity, "total": total}
                    trade_data.append(data)
                    self.order(data)


                    if profitable: print("\tProfit Captured Per Share Sold: ", sale_price-purchase_price) # If profitable, output the profit captured per share sold
                    open = False

        # Create response package
        response = {}
        response["ending_aum"] = aum
        response["dollar_change"] = response["ending_aum"] - setting_values["starting_aum"]
        response["percent_change"] = (response["dollar_change"]/setting_values["starting_aum"])*100
        response["setting_id"] = setting_id
        self.handler.execute(queries.create_performance, values=response)
        del response['setting_id']
        response["price_data"] = df
        # Add the trade data to the response package
        response["trade_data"] = pd.DataFrame(trade_data)

        return response
    
    def simulate(self): # NOTE: We can worry about this after we build backtest! This is for realtime simulation!
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        # This would use realtime price data which would be added to (or retrived from) the appropriate collection or database or dataframe in market
        # It would perform the required calculations based on the confiurations
        
        # Realtime (simualted) testing code here

        # This would take a setting and a configuration as well
        # It should output performance and market data (including price data) as pandas df or a list of dictionaries?
        return

    # Prints an overview of the market/performances etc. (can use complex MySQL queries and create visualizations now)
    def __str__(self):
        return("working")