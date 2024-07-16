CREATE DATABASE IF NOT EXISTS `msci-436-project`;

USE `msci-436-project`;

CREATE TABLE IF NOT EXISTS `ticker` (
    `name` varchar(255) NOT NULL,
    `symbol` varchar(10) NOT NULL,
    `created_at` datetime NOT NULL,
    PRIMARY KEY (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `trade` (
    `id` UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    `symbol` varchar(10) NOT NULL,
    `price` decimal(10,2) NOT NULL,
    `position` varchar(1) NOT NULL, -- 'b' or 's'
    `created_at` datetime NOT NULL,
    `user` varchar(255) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `symbol` (`symbol`),
    CONSTRAINT `trade_ibfk_1` FOREIGN KEY (`symbol`) REFERENCES `ticker` (`symbol`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Queries -----------------------------------

-- Today's trades for a single ticker
SELECT * 
FROM trade 
WHERE symbol = 'tsla' 
    AND DATE(created_at) = CURDATE();

-- All trades for a ticker
SELECT * 
FROM trade 
WHERE symbol = 'ticker_symbol';



