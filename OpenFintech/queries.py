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