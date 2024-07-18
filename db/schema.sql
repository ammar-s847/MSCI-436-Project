-- Create the database (this part usually done from a superuser context or via a separate command)
-- CREATE DATABASE "msci-436-project"; 

-- Connect to the database
\c "msci-436-project"

-- Create the ticker table
CREATE TABLE IF NOT EXISTS ticker (
    name varchar(255) NOT NULL,
    symbol varchar(10) NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY (symbol)
);

-- Create the trade table
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
