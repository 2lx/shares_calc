-- Shares
CREATE TABLE IF NOT EXISTS Share(
    Name VARCHAR(60),
    Abbr VARCHAR(10) UNIQUE
);

INSERT INTO Share (Name, Abbr)
VALUES ("Advanced Micro Devices, Inc.", "AMD");

-- Markets
CREATE TABLE IF NOT EXISTS Market(
    Name VARCHAR(60),
    Abbr VARCHAR(10) UNIQUE
);

INSERT INTO Market (Name, Abbr)
SELECT "Санкт-Петербургская Биржа", "SPBEX" UNION ALL
SELECT "Акции США (BATS)", "US1";

-- Times
CREATE TABLE IF NOT EXISTS Time(
    Hours INTEGER,
    Minutes INTEGER
);
CREATE UNIQUE INDEX IF NOT EXISTS TimeUniqueHoursMinutes ON Time(Hours, Minutes);

INSERT INTO Time (Hours, Minutes)
SELECT Hours.x, Minutes.x
FROM (WITH RECURSIVE
      Counter(x) AS (SELECT 0 UNION ALL SELECT x + 1 FROM Counter LIMIT 24)
      SELECT x FROM Counter) AS Hours
CROSS JOIN
     (WITH RECURSIVE
      Counter(x) AS (SELECT 0 UNION ALL SELECT x + 5 FROM Counter LIMIT 60 / 5)
      SELECT x FROM Counter) AS Minutes
ORDER BY Hours.x, Minutes.x;

-- Quotations
CREATE TABLE IF NOT EXISTS Quotation(
    MarketId INTEGER,
    ShareId INTEGER,
    DateTime INTEGER,
--    TimeId INTEGER,
    OpenPrice REAL,
    HighPrice REAL,
    LowPrice REAL,
    ClosePrice REAL,
    Volume INTEGER,
    FOREIGN KEY (MarketId) REFERENCES Market(Id),
    FOREIGN KEY (ShareId) REFERENCES Share(Id)
--    FOREIGN KEY (TimeId) REFERENCES Time(Id),
);
CREATE UNIQUE INDEX IF NOT EXISTS QuotationUniqueShareMarketTime ON Quotation(ShareId, MarketId, DateTime);


