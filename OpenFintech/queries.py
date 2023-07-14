create_users_table = """CREATE TABLE users (
        user_id int NOT NULL AUTO_INCREMENT,
        date_created DATETIME DEFAULT now(),
        username varchar(255) UNIQUE NOT NULL,
        email varchar(255) UNIQUE DEFAULT NULL,
        password varchar(255) DEFAULT NULL,
        year int DEFAULT 0,
        major varchar(255) DEFAULT NULL,

        PRIMARY KEY (user_id),
        CHECK (year>=1)
        );"""

create_config_table = """CREATE TABLE configs ( 
        config_id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        ma_period_1 int DEFAULT 0,
        ma_period_2 int DEFAULT 0,
        ema_period_1 int DEFAULT 0,
        ema_period_2 int DEFAULT 0,
        rsi_length int DEFAULT 0,
        ma_length int DEFAULT 0,
        
        PRIMARY KEY (config_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);"""

create_performance_table = """CREATE TABLE configs ( 
        config_id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        ma_period_1 int DEFAULT 0,
        ma_period_2 int DEFAULT 0,
        ema_period_1 int DEFAULT 0,
        ema_period_2 int DEFAULT 0,
        rsi_length int DEFAULT 0,
        ma_length int DEFAULT 0,
        
        PRIMARY KEY (config_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);"""

create_setting_table = """CREATE TABLE settings ( 
        setting_id int NOT NULL AUTO_INCREMENT,
        user_id int NOT NULL,
        config_id int NOT NULL,
        date_created DATETIME DEFAULT now(),

        stop_loss int DEFAULT 0,
        ma_period_2 int DEFAULT 0,
        ema_period_1 int DEFAULT 0,
        ema_period_2 int DEFAULT 0,
        rsi_length int DEFAULT 0,
        ma_length int DEFAULT 0,
        
        PRIMARY KEY (config_id),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
);"""

create_trade_table = """CREATE TABLE users (
        user_id int PRIMARY KEY AUTO_INCREMENT,
        date_created DATETIME DEFAULT now(),
        username varchar(255) UNIQUE NOT NULL,
        email varchar(255) UNIQUE DEFAULT NULL,
        password varchar(255) DEFAULT NULL,
        year int DEFAULT 0,
        major varchar(255) DEFAULT NULL,
        CHECK (year>=1)
        );"""

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