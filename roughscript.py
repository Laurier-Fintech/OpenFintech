from OpenFintech import SQLite3, queries
from datetime import datetime as dt

handler = SQLite3(name="Test.db")
result = handler.execute(queries.performance_tbl_create)
result = handler.execute(queries.create_performance, values={
    'setting_id': 1,  # Assuming 1 as an example
    'dollar_change': 5.0,
    'percent_change': 5.0,
    'ending_aum': 1050.0
})
print(result)


result=handler.execute("SELECT * FROM performances", query=True)
print(result)
handler.disconnect()