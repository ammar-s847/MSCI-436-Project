import psycopg2
from psycopg2 import sql

# Database connection parameters
conn_params = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'u472h46a',
    'host': 'localhost',
    'port': '5432'
}

# Connect to PostgreSQL
conn = psycopg2.connect(**conn_params)
conn.autocommit = True
cur = conn.cursor()

# Create the new database
cur.execute("CREATE DATABASE \"msci-436-project\"")

# Close connection to 'postgres' database
cur.close()
conn.close()

# Connect to the new database
conn_params['dbname'] = 'msci-436-project'
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()

# Schema SQL
schema_sql = """
CREATE TABLE IF NOT EXISTS ticker (
    name varchar(255) NOT NULL,
    symbol varchar(10) NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (symbol)
);

CREATE TABLE IF NOT EXISTS trade (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    symbol varchar(10) NOT NULL,
    price decimal(10,2) NOT NULL,
    position varchar(1) NOT NULL, -- 'b' or 's'
    created_at timestamp NOT NULL,
    "user" varchar(255) NOT NULL,
    CONSTRAINT trade_ibfk_1 FOREIGN KEY (symbol) REFERENCES ticker (symbol)
);

-- Queries -----------------------------------

-- Today's trades for a single ticker
SELECT * 
FROM trade 
WHERE symbol = 'tsla' 
    AND DATE(created_at) = CURRENT_DATE;

-- All trades for a ticker
SELECT * 
FROM trade 
WHERE symbol = 'ticker_symbol';
"""

# Execute the schema SQL
cur.execute(schema_sql)
conn.commit()

# Close the connection
cur.close()
conn.close()
