# NOTE: SQLITE3 QUERIES
user_tbl_create = """
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE DEFAULT NULL,
    password TEXT DEFAULT NULL,
    year INTEGER DEFAULT NULL,
    major TEXT DEFAULT NULL,
    CHECK (year >= 1 OR year IS NULL)
);
"""
create_user = """INSERT INTO users(username, email, password, year, major) VALUES(:username, :email, :password, :year, :major)"""

settings_tbl_create = """
CREATE TABLE IF NOT EXISTS settings ( 
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,

    ticker TEXT NOT NULL,

    short TEXT DEFAULT NULL,
    long_ TEXT DEFAULT NULL,

    stop_loss REAL DEFAULT 0,
    starting_aum REAL DEFAULT 0,
    take_profit REAL DEFAULT 0,

    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
create_setting = """INSERT INTO settings(user_id, ticker, short, long_, stop_loss, starting_aum, take_profit) VALUES(:user_id, :ticker, :short, :long_, :stop_loss, :starting_aum, :take_profit)"""

trades_tbl_create = """
CREATE TABLE IF NOT EXISTS trades ( 
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_id INTEGER NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,

    type INTEGER NOT NULL,
    trade_dt DATETIME NOT NULL,

    price REAL NOT NULL,
    quantity REAL NOT NULL,
    total REAL NOT NULL,

    FOREIGN KEY (setting_id) REFERENCES settings (setting_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
create_trade = """INSERT INTO trades(setting_id, type, trade_dt, price, quantity, total) VALUES(:setting_id, :type, :trade_dt, :price, :quantity, :total)"""

performance_tbl_create = """
CREATE TABLE IF NOT EXISTS performances ( 
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_id INTEGER NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,

    dollar_change REAL DEFAULT 0,
    percent_change REAL DEFAULT 0,
    ending_aum REAL DEFAULT 0,

    FOREIGN KEY (setting_id) REFERENCES settings (setting_id) ON DELETE CASCADE ON UPDATE CASCADE
);
"""
create_performance = """INSERT INTO performances(setting_id, dollar_change, percent_change, ending_aum) VALUES(:setting_id, :dollar_change, :percent_change, :ending_aum)"""


# NOTE: MYSQL QUERIES
# Table Creation Queries
create_equity_table = """CREATE TABLE equities (
        equity_id int NOT NULL AUTO_INCREMENT,
        ticker varchar(255) UNIQUE NOT NULL,
        date_created DATETIME DEFAULT now(),

        name varchar(255) DEFAULT NULL,
        description LONGTEXT DEFAULT NULL,
        cik varchar(255) DEFAULT NULL,

        country varchar(255) DEFAULT NULL,
        currency varchar(255) DEFAULT NULL,
        exchange varchar(255) DEFAULT NULL,
        address varchar(255) DEFAULT NULL,
        industry varchar(255) DEFAULT NULL,
        sector varchar(255) DEFAULT NULL,
        
        PRIMARY KEY (equity_id)
);"""

create_users_table = """CREATE TABLE users (
        user_id int AUTO_INCREMENT,
        date_created DATETIME DEFAULT now(),
        username varchar(255) UNIQUE NOT NULL,
        email varchar(255) UNIQUE DEFAULT NULL,
        password varchar(255) DEFAULT NULL,
        year int DEFAULT NULL,
        major varchar(255) DEFAULT NULL,

        PRIMARY KEY (user_id),
        CHECK (year>=1 OR NULL)
);"""

create_setting_table = """CREATE TABLE settings ( 
        setting_id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        ticker varchar(50) NOT NULL,

        short varchar(50) DEFAULT NULL,
        long_ varchar(50) DEFAULT NULL,

        stop_loss float DEFAULT 0,
        starting_aum float DEFAULT 0,
        take_profit float DEFAULT 0,
        
        chart_date_range_start DATETIME DEFAULT NULL,
        chart_date_range_end DATETIME DEFAULT NULL,
        chart_freq_mins BIGINT DEFAULT NULL,
        
        PRIMARY KEY (setting_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);"""

create_performance_table = """CREATE TABLE performances ( 
        performance_id int NOT NULL AUTO_INCREMENT,
        setting_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        dollar_change float DEFAULT 0,
        percent_change float DEFAULT 0,
        ending_aum float DEFAULT 0,
        
        PRIMARY KEY (performance_id),
        FOREIGN KEY (setting_id) REFERENCES settings (setting_id) ON DELETE CASCADE ON UPDATE CASCADE
);"""

create_trade_table = """CREATE TABLE trades ( 
        trade_id int NOT NULL AUTO_INCREMENT,
        setting_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        type int NOT NULL,
        trade_dt DATETIME NOT NULL,

        price float NOT NULL,
        quantity float NOT NULL,
        total float NOT NULL,
        
        PRIMARY KEY (trade_id),
        FOREIGN KEY (setting_id) REFERENCES settings (setting_id) ON DELETE CASCADE ON UPDATE CASCADE
);"""

# User Insertion Queries
insert_simple_user = "INSERT INTO users (username) VALUES (%s)"
insert_complete_user = "INSERT INTO users (username, email, password, year, major) VALUES (%s,%s,%s,%s,%s)"

# Model Insertion Queries
insert_setting_entry = """ INSERT INTO settings (
        user_id, ticker, short, long_, stop_loss, take_profit, starting_aum , chart_freq_mins)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
"""

# Equity Insertion Query
insert_equity_complete = "INSERT INTO equities (ticker, name, description, cik, country, currency, exchange, address, industry, sector) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
insert_equity_short = "INSERT INTO equities (ticker) VALUES (%s)"

# Trade Insertion Query
insert_trade_entry = """ INSERT INTO trades (
        setting_id, type, trade_dt, price, quantity, total) VALUES (%s,%s,%s,%s,%s,%s);
"""

# Equities Selection Queries
select_ticker_entry = "SELECT * FROM equities WHERE ticker=%s" # Enforce sort by the latest (so we get the last entry)

# Performance entry query
insert_performance_entry = "INSERT INTO performances (setting_id, dollar_change, percent_change, ending_aum) VALUES (%s, %s, %s, %s)"