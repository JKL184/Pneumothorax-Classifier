CREATE DATABASE lungify;
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
