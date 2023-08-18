from .Databases import MySQL
from .APIs import Alphavantage
from . import queries
import copy

# TODO:
# Configuration CRUD functions
# Implement test_config based on the provided notes
# Implement the __str__ function

class Model:
    def __init__(self, database):
        self.db_handler = database
        return
    
    def create(self,values:dict): # Function used to create a settings entry
        # Convert values dict to a set
        values=(values["user_id"],values["equity_id"], values["short"], values["long"],
                values["stop_loss"],values["take_profit"],values["starting_aum"],
                values["chart_freq_mins"])
        self.db_handler.execute(queries.insert_setting_entry, values)
        query_last = "SELECT LAST_INSERT_ID();"
        config_id = self.db_handler.execute(query_last, query=True)[0][0]
        return config_id

    def buy(self, values:dict):
        self.db_handler.execute(queries.insert_trade_entry, ())
        return
    
    def sell(self):
        return

    # The testing and running of configuation relies on the Market model.
    def backtest(self, setting_values:dict, api_handler:Alphavantage) -> dict:
        print("\nModel.backtest():")

        # Replace ticker with the equity_id
        ticker = setting_values.pop("ticker") # Remove ticker from the setting_values dict
        response = api_handler.overview(ticker) # Retrive its last appropriate entry from the db (or request data from Alphavantage and create entry in DB)
        setting_values["equity_id"] = response[0] # Add the equity_id to the setting_values dict
        
        # Create a entry to the settings table
        setting_id = self.create(setting_values)
        print(f"\tCreated setting with the ID {setting_id}")

        # Import the data for given the setting using the given api_handler (Alphavantage object)
        df = Alphavantage.equity_daily(key=Alphavantage.get_key(api_handler.keys), ticker=ticker)
        print("\tPrice Data:")
        print(df)

        # Modify the price_data_df based on the given config values indicators section
        indicators = [''.join(setting_values["short"].split(" ")),''.join(setting_values["long"].split(" "))]
        df = api_handler.technical_indicator(indicators,df)
        print("\tPrice Data + Indicator Data:")
        print(df)
    
        # Get additional required info from settings
        aum = float(setting_values["starting_aum"])
        stop_loss = float(setting_values["stop_loss"])
        take_profit = float(setting_values["take_profit"])

        # Intiailize variables to store temp values to help the algorithm perform calculations
        open = False 
        quantity, purchase_price, sale_price = 0, 0, 0
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
                    print(i, ": Buy @", purchase_price, " AUM:", aum)
                    
                    # Create buy trade entry
                    self.buy({"setting_id": setting_id, "type": 0, "trade_dt": i, 
                              "price": purchase_price, "quantity":quantity, "total": total})
                    
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
                    print(i, ": Sell for", sale_price, " AUM:",aum, " Profitable: ",profitable)
                    
                    # Create sale trade entry

                    
                    
                    if profitable: print("\tProfit Captured Per Share Sold: ", sale_price-purchase_price) # If profitable, output the profit captured per share sold
                    open = False

        # Add a log of the trades for the current session to the response dictoinary
        
        print(f"Final AUM: {aum}")


        #df.to_csv("sample_model_data.csv", encoding='utf-8') 
        # Add price data to the response dictionary

        # Calculate performance data
        # Performance data should contain:
        #       Ending_aum
        #       percent_change
        #       dollar_change
        #       setting_id
        # Add the required fields and then create a performance entry to the performance table (database)
        # remove the fields not required for the response dictionary
        # Pack performance data into the response dictionary

        # Return response dictionary
        return
    
    def simulate(self): # NOTE: We can worry about this after we build backtest
        # Similar to “test_configuration” but for real-time (simulated market) testing. 
        # This would use realtime price data which would be added to (or retrived from) the appropriate collection or database or dataframe in market
        # It would perform the required calculations based on the confiurations
        
        # Realtime (simualted) testing code here

        # This would take a setting and a configuration as well
        # It should output performance and market data (including price data) as pandas df or a list of dictionaries?
        return

    # Prints the market overview specific to the model and configurations. (can use SQL complex queries and create visualizations now)
    def __str__(self):
        return("working")