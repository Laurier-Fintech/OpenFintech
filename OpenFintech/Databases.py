import mysql.connector

class MongoDB: # TODO: Simplified implementation of our FinMongo code
    def __init__():
        return

class MySQL:
    def __init__(self, host:str, user:str, password:str, database:str):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.curr = self.conn.cursor()
        return

    # Function that can execute statements with no values, one value, or multiple values (regardless of create, delete, etc as long as it follows MySQL's prepared statement conventions and packs multiple values in a list of sets and single entry values in just a set)
    def execute(self, statement:str, values=[], multiple=False, query=False):

        success=False
        try:
            # For handling multiple values that need to be binded to the prepared (and passed) statement/query before being executed
            if multiple:
                # If many values are provided, then iterate over the values and execute them with the statement (using executemany)
                if len(values)==0: raise Exception("Please provide values to insert multiple SQL entires.")
                for value in values: self.curr.executemany(statement,value)
            
            # For handling statements/queries that have no values or one set of values
            else: 
                if len(values)==0: self.curr.execute(statement)  # When no values are given, simply call execute
                
                else:
                    # Check if the given values are in a set (required by MySQL connector)
                    if isinstance(values, tuple)!=True: raise Exception("Given values must be in a set to be executed.")
                    self.curr.execute(statement,values) # Bind values to statement and execute

            if not query: 
                self.conn.commit() # Commit new insertations/changes
                success=True # Update success status to return True
            else: 
                success = response = self.curr.fetchall()

        except Exception as e: 
            print(e) # Can call destructor or handle error differently in the future
            pass

        return success

    # Function that closes the currsor and disconnects the MySQL connection
    def disconnect(self)->bool: 
        success = True
        try:
            self.curr.close()
            self.conn.disconnect()
        except: success=False
        return success

    # Function that returns the list of tables in the database
    def __str__(self)->str:
        tables = "Tables:\n"
        self.curr.execute("SHOW TABLES")
        for tableName in self.curr: tables+= f"\t{tableName}\n"
        return tables

if __name__=="__main__":
    import queries
    import os 
    from dotenv import load_dotenv
    load_dotenv()
    SQL_USER = os.getenv('MYSQL_USER')
    SQL_PASS = os.getenv('MYSQL_PASS') 
    host = "openfintech.cbbhaex7aera.us-east-2.rds.amazonaws.com"
    handler = MySQL(host=host,user=SQL_USER,password=SQL_PASS,database="main")
    
    
    #handler.curr.execute(queries.create_users_table)
    #handler.curr.execute(queries.create_equity_table)
    #handler.curr.execute(queries.create_config_table)
    #handler.curr.execute(queries.create_setting_table)
    #handler.curr.execute(queries.create_trade_table)
    #handler.curr.execute(queries.create_performance_table)
    
    sample_overview_data = {
    "Symbol": "IBM",
    "AssetType": "Common Stock",
    "Name": "International Business Machines",
    "Description": "International Business Machines Corporation (IBM) is an American multinational technology company headquartered in Armonk, New York, with operations in over 170 countries. The company began in 1911, founded in Endicott, New York, as the Computing-Tabulating-Recording Company (CTR) and was renamed International Business Machines in 1924. IBM is incorporated in New York. IBM produces and sells computer hardware, middleware and software, and provides hosting and consulting services in areas ranging from mainframe computers to nanotechnology. IBM is also a major research organization, holding the record for most annual U.S. patents generated by a business (as of 2020) for 28 consecutive years. Inventions by IBM include the automated teller machine (ATM), the floppy disk, the hard disk drive, the magnetic stripe card, the relational database, the SQL programming language, the UPC barcode, and dynamic random-access memory (DRAM). The IBM mainframe, exemplified by the System/360, was the dominant computing platform during the 1960s and 1970s.",
    "CIK": "51143",
    "Exchange": "NYSE",
    "Currency": "USD",
    "Country": "USA",
    "Sector": "TECHNOLOGY",
    "Industry": "COMPUTER & OFFICE EQUIPMENT",
    "Address": "1 NEW ORCHARD ROAD, ARMONK, NY, US",
    "FiscalYearEnd": "December",
    "LatestQuarter": "2023-03-31",
    "MarketCapitalization": "121133300000",
    "EBITDA": "12644000000",
    "PERatio": "15.99",
    "PEGRatio": "1.276",
    "BookValue": "23.79",
    "DividendPerShare": "6.6",
    "DividendYield": "0.0498",
    "EPS": "1.873",
    "RevenuePerShareTTM": "66.97",
    "ProfitMargin": "0.0303",
    "OperatingMarginTTM": "0.132",
    "ReturnOnAssetsTTM": "0.0376",
    "ReturnOnEquityTTM": "9.85",
    "RevenueTTM": "60585001000",
    "GrossProfitTTM": "32688000000",
    "DilutedEPSTTM": "2.24",
    "QuarterlyEarningsGrowthYOY": "0.253",
    "QuarterlyRevenueGrowthYOY": "0.004",
    "AnalystTargetPrice": "141.06",
    "TrailingPE": "59.55",
    "ForwardPE": "15.55",
    "PriceToSalesRatioTTM": "2.108",
    "PriceToBookRatio": "6.75",
    "EVToRevenue": "2.969",
    "EVToEBITDA": "25.81",
    "Beta": "0.848",
    "52WeekHigh": "149.31",
    "52WeekLow": "111.29",
    "50DayMovingAverage": "130.26",
    "200DayMovingAverage": "133.35",
    "SharesOutstanding": "908045000",
    "DividendDate": "2023-06-10",
    "ExDividendDate": "2023-05-09"
    }
    """success = handler.execute(queries.insert_equity_complete, values=
        (
            sample_overview_data["Symbol"],
            sample_overview_data["Name"],
            sample_overview_data["Description"],
            sample_overview_data["CIK"],
            sample_overview_data["Country"],
            sample_overview_data["Currency"],
            sample_overview_data["Exchange"],
            sample_overview_data["Address"],
            sample_overview_data["Industry"],
            sample_overview_data["Sector"],
        )
    )
    print(success)"""
    
    response = handler.execute(queries.select_ticker_entry, values=("IBM",), query=True)
    print(type(response))
    print(response[0][2])

    handler.disconnect()