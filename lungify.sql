CREATE DATABASE lungify;
USE lunify;


-- creating tables

CREATE TABLE scans_table (
	EmployeeID VARCHAR(30),
	PatientID VARCHAR(30),
    xray_format VARCHAR(50),
    ResultID VARCHAR (100),
    PRIMARY KEY (EmployeeID)
);

CREATE TABLE result_table (
	ResultID VARCHAR(30),
	PatientID VARCHAR(30),
    identification VARCHAR(50),
    classification VARCHAR (100),
    expert_name VARCHAR(100),
    PRIMARY KEY (ResultID)
);

CREATE TABLE expert_table (
	expert_name VARCHAR(100),
	expert_email_address VARCHAR(255),
    PRIMARY KEY (expert_email_address)
);

CREATE TABLE outline (
	ResultID VARCHAR(30),
    identification VARCHAR(50),
    classification VARCHAR (100),
    PRIMARY KEY (ResultID)
);

CREATE TABLE users (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);


-- altering tables 

ALTER TABLE scans_table
RENAME TO xrays;

ALTER TABLE result_table
RENAME TO results;

ALTER TABLE expert_table
RENAME TO experts;

ALTER TABLE results
ADD size int; 


-- creating views

CREATE VIEW Positive_Cases AS 
SELECT PatientID, identification, classification
FROM results
WHERE identification = 'Positive';

CREATE VIEW Negative_Cases AS 
SELECT PatientID, identification
FROM results
WHERE identification = 'Negative';

ALTER VIEW Positive_Cases AS 
SELECT PatientID, identification, classification, size
FROM results
WHERE identification = 'Positive';

CREATE VIEW Small_Cases AS 
SELECT PatientID, size
FROM results
WHERE identification = 'Positive' and classification = 'Small';

CREATE VIEW Large_Cases AS 
SELECT PatientID, size
FROM results
WHERE identification = 'Positive' and classification = 'Large';
