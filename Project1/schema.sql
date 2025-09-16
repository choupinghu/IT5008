/*******************

  Create the schema.

********************/
CREATE TABLE IF NOT EXISTS cuisine(
    CuisineCountry VARCHAR(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS menu (
    Item VARCHAR(20) PRIMARY KEY,
    Price DECIMAL(5,2) NOT NULL,
    CuisineCountry VARCHAR(20) NOT NULL
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
    Phone VARCHAR(10) PRIMARY KEY,
    Firstname VARCHAR(20),
    Lastname VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS orderinfo(
    OrderDate DATE NOT NULL,
    OrderTime TIME NOT NULL,
    OrderID VARCHAR(15) PRIMARY KEY,
    Payment VARCHAR(4) CHECK(Payment = 'card' OR Payment = 'cash') NOT NULL,
    CardNo VARCHAR(19),
    CardType VARCHAR(15),
    TotalPrice DECIMAL(5,2) NOT NULL,
    Phone VARCHAR(10),
    Firstname VARCHAR(20), 
    Lastname VARCHAR(20)
);

CREATE TABLE orderitems (
    OrderID VARCHAR(15) REFERENCES orderinfo(OrderID) ON DELETE CASCADE,
    Item VARCHAR(100),
    StaffID VARCHAR(10),
	Quantity INT NOT NULL DEFAULT 1,
	
    PRIMARY KEY (OrderID, Item, StaffID),
	CONSTRAINT fk_staff 
		FOREIGN KEY (StaffID) REFERENCES staff(StaffID) 
		ON UPDATE CASCADE
);
