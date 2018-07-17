CREATE TABLE Admin (Email       VARCHAR(255)       PRIMARY KEY,
                    Password    VARCHAR(255)       NOT NULL
);

CREATE TABLE Visitor (Email        VARCHAR(255)    PRIMARY KEY,
                      Password     VARCHAR(255)    NOT NULL,
                      CardNumber   CHAR(16)        NOT NULL     UNIQUE,
                      Month        TINY INT        NOT NULL,
                      Year         CHAR(4)         NOT NULL,
                      CVV          SMALL INT       NOT NULL,
                      IsCurator    BIT             NOT NULL,
                      CONSTRAINT CHK_CVV CHECK (CVV BETWEEN 100 AND 9999),
                      CONSTRAINT CHK_Month (CHECK Month BETWEEN 1 AND 31)
);

CREATE TABLE Museum (MuseumName     VARCHAR(255)     PRIMARY KEY, 
                     AdminEmail     VARCHAR(255)     NOT NULL
);

CREATE TABLE CuratorRequest (MuseumName         VARCHAR(255),
                             VisitorEmail       VARCHAR(255),
                             PRIMARY KEY(MuseumName, VisitorEmail), 
                             FOREIGN KEY (MuseumName) REFERENCES Museum(MuseumName), 
                             FOREIGN KEY (VisitorEmail) REFERENCES Visitor(Email)
);

CREATE TABLE Review (MuseumName         VARCHAR(255),
                     VisitorEmail       VARCHAR(255),
                     Comment            VARCHAR(4096),
                     Rating             TINYINT,
                     PRIMARY KEY(MuseumName, VisitorEmail),
                     FOREIGN KEY (MuseumName) REFERENCES Museum(MuseumName),
                     FOREIGN KEY (VisitorEmail) REFERENCES Visitor(Email),
                     CONSTRAINT CHK_Rating CHECK Rating BETWEEN 1 AND 5
);

CREATE TABLE Ticket (MuseumName        VARCHAR(255),
                     VisitorEmail      VARCHAR(255),
                     Price             DECIMAL(7,2),
                     PurchaseTimeStamp DATETIME,
                     PRIMARY KEY(MuseumName, VisitorEmail),
                     FOREIGN KEY (MuseumName) REFERENCES Museum(MuseumName),
                     FOREIGN KEY (VisitorEmail) REFERENCES Visitor(Email)
);

CREATE TABLE Exhibit (MuseumName        VARCHAR(255),
                      ExhibitName       VARCHAR(255),
                      Year              CHAR(4),
                      URL               VARCHAR(2083),
                      CuratorEmail      VARCHAR(255)    NOT NULL,
                      PRIMARY KEY(MuseumName, ExhibitName),
                      FOREIGN KEY (MuseumName) REFERENCES Museum(MuseumName)
                      FOREIGN KEY (CuratorEmail) REFERENCES Visitor (Email)
);
