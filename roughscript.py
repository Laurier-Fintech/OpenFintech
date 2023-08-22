from OpenFintech import SQLite3, queries

handler = SQLite3(name="Test.db")
result = handler.execute(queries.settings_tbl_create,query=False)
result = handler.execute(queries.settings_create, values={
    'user_id':1,'ticker':'TSLA','short':'EMA 3','long_':'EMA 10','stop_loss':0.10,'starting_aum':100000,'take_profit':0.5
})
print(result)


result=handler.execute("SELECT * FROM settings")
print(result)
handler.disconnect()