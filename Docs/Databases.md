## **MySQL and MongoDB Python Wrapper**

### **Introduction**:

This documentation describes a simple Python wrapper around MySQL and MongoDB functionalities, enabling database operations with minimal code.

For MongoDB, the class is a placeholder and further implementation details will be provided later.

### **Classes**:

#### **1. MongoDB**

A placeholder class representing MongoDB operations. 

*Note: This class is yet to be fully implemented.*

```python
class MongoDB:
    ...
```

#### **2. MySQL**

A Python class encapsulating various operations with a MySQL database.

##### **Instantiation**:

Connect to a MySQL database:

```python
from OpenFintech import MySQL

db_instance = MySQL(host="your_host", user="your_username", password="your_password", database="your_db_name")
```

##### **Methods**:

###### **execute**

This method is designed to handle various SQL operations:

- **For simple queries without any values**:
  
  ```python
  db_instance.execute("CREATE TABLE example (id INT, name VARCHAR(255))")
  ```

- **For queries requiring a single set of values**:
  
  ```python
  db_instance.execute("INSERT INTO example (id, name) VALUES (%s, %s)", (1, "John"))
  ```

- **For multiple insertions**:
  
  ```python
  values_to_insert = [(2, "Jane"), (3, "Doe")]
  db_instance.execute("INSERT INTO example (id, name) VALUES (%s, %s)", values=values_to_insert, multiple=True)
  ```

###### **disconnect**

Disconnect from the MySQL server:

```python
db_instance.disconnect()
```

###### **\_\_str__**

Returns a string representation listing all tables in the connected database:

```python
print(db_instance)
```

### **Usage and Notes**:

When interacting with the database, always ensure to use the `execute` function appropriately, respecting the SQL conventions. To ensure data integrity, always disconnect from the database once operations are completed.