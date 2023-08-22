from OpenFintech import SQLite3, queries
from datetime import datetime as dt

handler = SQLite3(name="Test.db")
result = handler.execute(queries.trades_tbl_create,query=False)
result = handler.execute(queries.create_trade, values={
    'setting_id':1,'type':1,'trade_dt':dt.now(),'price':10, 'quantity':10,'total':100
})
print(result)


result=handler.execute("SELECT * FROM trades")
print(result)
handler.disconnect()