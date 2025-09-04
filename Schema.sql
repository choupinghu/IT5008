/*******************

  Create the schema.

********************/
CREATE TABLE IF NOT EXISTS cuisine(
    CuisineCountry VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS menu (
    Item VARCHAR(20) PRIMARY KEY,
    Price DECIMAL(5,2) NOT NULL,
    CuisineCountry VARCHAR(20),
    FOREIGN KEY (CuisineCountry) REFERENCES cuisine(CuisineCountry)
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS staff(
    StaffID VARCHAR(8) PRIMARY KEY,
    Name VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS staff_cuisine(
    StaffID VARCHAR(8) NOT NULL,
    CuisineCountry VARCHAR(20),
    PRIMARY KEY (StaffID, CuisineCountry),
    FOREIGN KEY (StaffID) REFERENCES staff(StaffID),
    FOREIGN KEY (CuisineCountry) REFERENCES cuisine(CuisineCountry)
);

CREATE TABLE IF NOT EXISTS registration(
    CallDate DATE,
    CallTime TIME,
    Phone VARCHAR(8) PRIMARY KEY,
    Firstname VARCHAR(20),
    Lastname VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS orderinfo(
    OrderDate DATE NOT NULL,
    OrderTime TIME NOT NULL,
    OrderID VARCHAR(10) PRIMARY KEY,
    Payment VARCHAR(4) CHECK(Payment = 'card' OR Payment = 'cash') NOT NULL,
    CardNo VARCHAR(19),
    CardType VARCHAR(15),
    Item VARCHAR(20) NOT NULL,
    TotalPrice DECIMAL(5,2) NOT NULL,
    Phone VARCHAR(8),
    Firstname VARCHAR(20), 
    Lastname VARCHAR(20),
    StaffID VARCHAR(8) NOT NULL,
    
    FOREIGN KEY (StaffID) REFERENCES staff(StaffID)
        ON UPDATE CASCADE,
    FOREIGN KEY (Item) REFERENCES menu(Item)
        ON UPDATE CASCADE,
    FOREIGN KEY (Phone) REFERENCES registration(Phone)
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS orderitems(
    OrderItemID SERIAL PRIMARY KEY,
    OrderID VARCHAR(10) NOT NULL,
    Item VARCHAR(20) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES orderinfo(OrderID)
        ON UPDATE CASCADE,
    FOREIGN KEY (Item) REFERENCES menu(Item)
        ON UPDATE CASCADE
);
