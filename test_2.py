from OpenFintech import Alphavantage

df = Alphavantage.equity_daily(key="NDYBGSF1PGZROO4Q",ticker="AAPL")
print(df)