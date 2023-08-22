from OpenFintech import SQLite3, queries

handler = SQLite3(name="Test.db")
result = handler.execute(queries.user_tbl_create,query=False)
result = handler.execute(queries.user_create, values={
    'username':"John",'email':None,'password':None,'year':None,'major':None
})
print(result)


result=handler.execute("SELECT * FROM users")
print(result)
handler.disconnect()