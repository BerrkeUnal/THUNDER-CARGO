CREATE DATABASE CargoSystem;
USE  CargoSystem;

/* CREATING TABLES*/
CREATE TABLE CargoStatusType(
	StatusID char(5) not null,
    StatusDescription varchar(50) not null,
    PRIMARY KEY(StatusID)
);

CREATE TABLE EmployeeRoles(
	RoleID char(5) not null,
    RoleName varchar(50) not null,
    PRIMARY KEY(RoleID)
);

CREATE TABLE ServiceTypes(
	ServiceTypeID char(5) not null,
    ServiceType varchar(50) not null,
    PRIMARY KEY(ServiceTypeID)
);

CREATE TABLE CargoBranches(
	BranchID char(5) not null,
	BranchName varchar(50) not null,
	BranchNumber varchar(50) not null,
	BranchEmail varchar(50) not null,
	BranchCity varchar(50) not null,
	BranchDistrict varchar(50) not null,
	BranchAddress varchar(100) not null,
	PRIMARY KEY(BranchID)
);

CREATE TABLE Customers(
	CustID char(5) not null,
	FirstName varchar(50) not null,
	LastName varchar(50) not null,
	CustNumber varchar(50) not null,
    Email varchar(100) null,
	Address varchar(50) not null,
	Country varchar(50) not null,
	City varchar(50) not null,
       Username varchar(50) not null,
       PasswordHash varchar(255) not null,
       LastLogin datetime null,
	PRIMARY KEY(CustID),
    UNIQUE(CustNumber),
    UNIQUE(Email),
    UNIQUE(Username)
);

CREATE TABLE Vehicles(
	VehicleID char(5) not null,
    LicensePlate varchar(10) not null,
    VehicleType varchar (20) not null,
    CurrentBranchID char(5) not null,
    UNIQUE(LicensePlate),
    PRIMARY KEY(VehicleID),
    FOREIGN KEY(CurrentBranchID) references CargoBranches(BranchID)
);

CREATE TABLE Manifests(
	ManifestID char(5) not null,
    VehicleID char(5) not null,
    DestBranchID char(5) not null,
    OriginBranchID char(5) not null,
    ArrivalTime datetime,
    DepartureTime datetime,
    PRIMARY KEY(ManifestID),
    FOREIGN KEY(DestBranchID) references CargoBranches(BranchID),
    FOREIGN KEY(OriginBranchID) references CargoBranches(BranchID)
);

CREATE TABLE Cargos(
    CargoID char(5) not null,
    ReceiverCustID char(5) not null,
    SenderCustID char(5) not null,
    CargoWeight decimal(10,2) not null,
    CargoLength decimal(10,2) not null,
    CargoWidth decimal(10,2) not null,
    CargoHeight decimal(10,2) not null,
    ShippingCost decimal(10,2) not null,
    OriginBranchID char(5) not null,
    DestBranchID char(5) not null,
    CurrentStatus varchar(50) not null,
    LastUpdated datetime,
    PaymentType varchar(50) not null,
    PaymentStatus varchar(50) not null,
    ServiceTypeID char(5) not null,
    PRIMARY KEY(CargoID),
    FOREIGN KEY(SenderCustID) references Customers(CustID),
    FOREIGN KEY(ReceiverCustID) references Customers(CustID),
    FOREIGN KEY(OriginBranchID) references CargoBranches(BranchID),
    FOREIGN KEY(DestBranchID) references CargoBranches(BranchID),
    FOREIGN KEY(ServiceTypeID) references ServiceTypes(ServiceTypeID)
);

CREATE TABLE ManifestCargo(
	ManifestID char(5) not null,
    CargoID char(5) not null,
    LogStatus varchar(50) default 'Loaded.' ,
    PRIMARY KEY(ManifestID, CargoID),
    FOREIGN KEY(ManifestID) references Manifests(ManifestID),
    FOREIGN KEY(CargoID) references Cargos(CargoID)
);

CREATE TABLE Employees(
	EmployeeID char(5) not null,
	EmployeeName varchar(50) not null,
	EmployeeLastName varchar(50) not null,
	EmployeeNumber varchar (50) not null,
	BranchID char(5) not null,
    RoleID char(5) not null,
    Username varchar(50) not null,
    PasswordHash varchar(255) not null,
    Salary varchar(50) not null,
    HireDate datetime,
    LastLogin datetime null,
    IsActive bit not null default 1,
	PRIMARY KEY(EmployeeID),
	FOREIGN KEY(BranchID) REFERENCES CargoBranches(BranchID),
    FOREIGN KEY(RoleID) REFERENCES EmployeeRoles(RoleID)
);

CREATE TABLE TrackingLog (
    TrackID CHAR(5) NOT NULL,
    LogTimestamps DATETIME NOT NULL,
    CargoID CHAR(5) NOT NULL,
    BranchID CHAR(5) NOT NULL,
    EmployeeID CHAR(5) NOT NULL,
    ReceiverName VARCHAR(100) NULL,
    ReceiverRelation VARCHAR(50) NULL,
    StatusID CHAR(5) NOT NULL,
    PRIMARY KEY (TrackID),
    FOREIGN KEY (CargoID)
        REFERENCES Cargos (CargoID),
    FOREIGN KEY (BranchID)
        REFERENCES CargoBranches (BranchID),
    FOREIGN KEY (EmployeeID)
        REFERENCES Employees (EmployeeID),
    FOREIGN KEY (StatusID)
        REFERENCES CargoStatusType (StatusID)
);

CREATE TABLE Invoice(
       InvoiceID char(5) not null,
       CargoID char(5) not null,
       CustID char(5) not null,
        InvoiceDate datetime,
        TotalAmount decimal(10,2) not null,
        PRIMARY KEY(InvoiceID),
        FOREIGN KEY(CargoID) references Cargos(CargoID),
       FOREIGN KEY(CustID) references Customers(CustID)
);

/* INSERTING VALUES */
INSERT INTO CargoStatusType (StatusID, StatusDescription) VALUES
('ST001', 'Order Created'),
('ST002', 'Picked Up from Sender'),
('ST003', 'Arrived at Origin Branch'),
('ST004', 'Loaded onto Vehicle'),
('ST005', 'In Transit'),
('ST006', 'Arrived at Transfer Center'),
('ST007', 'Departed from Transfer Center'),
('ST008', 'Arrived at Destination Branch'),
('ST009', 'Out for Delivery'),
('ST010', 'Delivered'),
('ST011', 'Recipient Not Home'),
('ST012', 'Address Not Found'),
('ST013', 'Damaged / Claim Processing'),
('ST014', 'Returned to Sender'),
('ST015', 'Lost in Transit');

INSERT INTO EmployeeRoles (RoleID, RoleName) VALUES
('RL001', 'General Manager'),
('RL002', 'Branch Manager'),
('RL003', 'Regional Manager'),
('RL004', 'Desk Officer'),
('RL005', 'Courier'),
('RL006', 'Truck Driver'),
('RL007', 'Moto Courier'),
('RL008', 'Warehouse Supervisor'),
('RL009', 'Warehouse Worker'),
('RL010', 'Customer Service Rep'),
('RL011', 'IT Specialist'),
('RL012', 'Accountant'),
('RL013', 'HR Specialist'),
('RL014', 'Security Guard'),
('RL015', 'Intern');

INSERT INTO ServiceTypes (ServiceTypeID, ServiceType) VALUES
('SV001', 'Standard Domestic'),
('SV002', 'Express Domestic'),
('SV003', 'Same Day Delivery'),
('SV004', 'Overnight Delivery'),
('SV005', 'Heavy Cargo'),
('SV006', 'Fragile Handling'),
('SV007', 'Document / File'),
('SV008', 'Cold Chain'),
('SV009', 'International Economy'),
('SV010', 'International Express'),
('SV011', 'Cash on Delivery'),
('SV012', 'Insurance Plus'),
('SV013', 'Palletized Freight'),
('SV014', 'E-Commerce Return'),
('SV015', 'VIP Secure Transport');

INSERT INTO CargoBranches (BranchID, BranchName, BranchNumber, BranchEmail, BranchCity, BranchDistrict, BranchAddress) VALUES
('BR001', 'Istanbul Central', '02120010001', 'ist.merkez@thunder.com', 'Istanbul', 'Maslak', 'Buyukdere Cad. No:1'),
('BR002', 'Istanbul Kadikoy', '02160010002', 'ist.kadikoy@thunder.com', 'Istanbul', 'Kadikoy', 'Bahariye Cad. No:15'),
('BR003', 'Istanbul Besiktas', '02120010003', 'ist.besiktas@thunder.com', 'Istanbul', 'Besiktas', 'Carsiici No:4'),
('BR004', 'Ankara Kizilay', '03120010004', 'ank.kizilay@thunder.com', 'Ankara', 'Cankaya', 'Ataturk Bulvari No:55'),
('BR005', 'Izmir Alsancak', '02320010005', 'izm.alsancak@thunder.com', 'Izmir', 'Konak', 'Kibris Sehitleri No:12'),
('BR006', 'Bursa Nilufer', '02240010006', 'bur.nilufer@thunder.com', 'Bursa', 'Nilufer', 'FSM Bulvari No:8'),
('BR007', 'Antalya Lara', '02420010007', 'ant.lara@thunder.com', 'Antalya', 'Muratpasa', 'Lara Yolu No:20'),
('BR008', 'Adana Seyhan', '03220010008', 'ada.seyhan@thunder.com', 'Adana', 'Seyhan', 'Ziyapasa Bulv. No:3'),
('BR009', 'Gaziantep Merkez', '03420010009', 'antep.mrkz@thunder.com', 'Gaziantep', 'Sehitkamil', 'Ipekyolu No:99'),
('BR010', 'Trabzon Meydan', '04620010010', 'trb.meydan@thunder.com', 'Trabzon', 'Ortahisar', 'Uzun Sokak No:5'),
('BR011', 'Eskisehir Odunpazari', '02220010011', 'esk.odun@thunder.com', 'Eskisehir', 'Odunpazari', 'Iki Eylul Cad. No:10'),
('BR012', 'Samsun Atakum', '03620010012', 'sam.atakum@thunder.com', 'Samsun', 'Atakum', 'Sahil Yolu No:45'),
('BR013', 'Konya Selcuklu', '03320010013', 'kon.selcuk@thunder.com', 'Konya', 'Selcuklu', 'Nalacaci Cad. No:22'),
('BR014', 'Kayseri Melikgazi', '03520010014', 'kay.melik@thunder.com', 'Kayseri', 'Melikgazi', 'Sivas Cad. No:30'),
('BR015', 'Mugla Bodrum', '02520010015', 'mug.bodrum@thunder.com', 'Mugla', 'Bodrum', 'Marina Cad. No:7');

INSERT INTO Customers (CustID, FirstName, LastName, CustNumber, Email, Address, Country, City, Username, PasswordHash, LastLogin) VALUES
('CU001', 'Ahmet', 'Yilmaz', '5321000001', 'ahmet.y@mail.com', 'Lale Sok. No:1', 'Turkey', 'Istanbul', 'ahmety', 'hash1', NOW()),
('CU002', 'Ayse', 'Demir', '5321000002', 'ayse.d@mail.com', 'Gul Apt. No:2', 'Turkey', 'Ankara', 'aysed', 'hash2', NOW()),
('CU003', 'Mehmet', 'Kaya', '5321000003', 'mehmet.k@mail.com', 'Menekse Cad. No:3', 'Turkey', 'Izmir', 'mehmetk', 'hash3', NULL),
('CU004', 'Fatma', 'Ozturk', '5321000004', 'fatma.o@mail.com', 'Papatya Sok. No:4', 'Turkey', 'Bursa', 'fatmao', 'hash4', NOW()),
('CU005', 'Mustafa', 'Celik', '5321000005', 'mustafa.c@mail.com', 'Susam Sok. No:5', 'Turkey', 'Antalya', 'mustafac', 'hash5', NULL),
('CU006', 'Zeynep', 'Arslan', '5321000006', 'zeynep.a@mail.com', 'Karanfil Apt. No:6', 'Turkey', 'Adana', 'zeynepa', 'hash6', NOW()),
('CU007', 'Emre', 'Polat', '5321000007', 'emre.p@mail.com', 'Begonya Cad. No:7', 'Turkey', 'Istanbul', 'emrep', 'hash7', NOW()),
('CU008', 'Selin', 'Koc', '5321000008', 'selin.k@mail.com', 'Manolya Sok. No:8', 'Turkey', 'Ankara', 'selink', 'hash8', NULL),
('CU009', 'Burak', 'Yildiz', '5321000009', 'burak.y@mail.com', 'Nilufer Apt. No:9', 'Turkey', 'Izmir', 'buraky', 'hash9', NOW()),
('CU010', 'Esra', 'Sahin', '5321000010', 'esra.s@mail.com', 'Zambak Cad. No:10', 'Turkey', 'Eskisehir', 'esras', 'hash10', NOW()),
('CU011', 'Can', 'Aydin', '5321000011', 'can.a@mail.com', 'Orkide Sok. No:11', 'Turkey', 'Trabzon', 'cana', 'hash11', NULL),
('CU012', 'Derya', 'Ozkan', '5321000012', 'derya.o@mail.com', 'Defne Apt. No:12', 'Turkey', 'Samsun', 'deryao', 'hash12', NOW()),
('CU013', 'Onur', 'Yavuz', '5321000013', 'onur.y@mail.com', 'Cinar Cad. No:13', 'Turkey', 'Gaziantep', 'onury', 'hash13', NOW()),
('CU014', 'Gamze', 'Bulut', '5321000014', 'gamze.b@mail.com', 'Selvi Sok. No:14', 'Turkey', 'Konya', 'gamzeb', 'hash14', NULL),
('CU015', 'Cem', 'Erkin', '5321000015', 'cem.e@mail.com', 'Ardic Apt. No:15', 'Turkey', 'Istanbul', 'ceme', 'hash15', NOW());

INSERT INTO Vehicles (VehicleID, LicensePlate, VehicleType, CurrentBranchID) VALUES
('VH001', '34TC001', 'Truck', 'BR001'),
('VH002', '34TC002', 'Van', 'BR001'),
('VH003', '34TC003', 'Motorcycle', 'BR001'),
('VH004', '06TC004', 'Truck', 'BR004'),
('VH005', '06TC005', 'Van', 'BR004'),
('VH006', '35TC006', 'Truck', 'BR005'),
('VH007', '35TC007', 'Motorcycle', 'BR005'),
('VH008', '16TC008', 'Van', 'BR006'),
('VH009', '07TC009', 'Van', 'BR007'),
('VH010', '01TC010', 'Truck', 'BR008'),
('VH011', '27TC011', 'Van', 'BR009'),
('VH012', '61TC012', 'Van', 'BR010'),
('VH013', '26TC013', 'Motorcycle', 'BR011'),
('VH014', '55TC014', 'Van', 'BR012'),
('VH015', '42TC015', 'Truck', 'BR013');

INSERT INTO Employees (EmployeeID, EmployeeName, EmployeeLastName, EmployeeNumber, BranchID, RoleID, Username, PasswordHash, Salary, HireDate, LastLogin, IsActive) VALUES
('EM001', 'Ali', 'Veli', 'EMP001', 'BR001', 'RL002', 'ali.v', 'pass1', '45000', '2022-01-15', NOW(), 1),
('EM002', 'Veli', 'Kirk', 'EMP002', 'BR001', 'RL004', 'veli.k', 'pass2', '32000', '2023-03-10', NOW(), 1),
('EM003', 'Ayse', 'Yil', 'EMP003', 'BR002', 'RL002', 'ayse.y', 'pass3', '42000', '2022-05-20', NOW(), 1),
('EM004', 'Fatma', 'Su', 'EMP004', 'BR002', 'RL005', 'fatma.s', 'pass4', '28000', '2024-01-05', NULL, 1),
('EM005', 'Hayri', 'Potur', 'EMP005', 'BR003', 'RL007', 'hayri.p', 'pass5', '30000', '2023-11-12', NOW(), 1),
('EM006', 'Mehmet', 'Can', 'EMP006', 'BR004', 'RL002', 'mehmet.c', 'pass6', '40000', '2021-08-01', NOW(), 1),
('EM007', 'Ceren', 'Tas', 'EMP007', 'BR004', 'RL004', 'ceren.t', 'pass7', '33000', '2023-02-14', NOW(), 1),
('EM008', 'Kaan', 'Boz', 'EMP008', 'BR005', 'RL006', 'kaan.b', 'pass8', '35000', '2022-09-30', NULL, 1),
('EM009', 'Lale', 'Gul', 'EMP009', 'BR006', 'RL002', 'lale.g', 'pass9', '41000', '2022-04-18', NOW(), 1),
('EM010', 'Sarp', 'Levend', 'EMP010', 'BR007', 'RL005', 'sarp.l', 'pass10', '29000', '2024-02-20', NOW(), 1),
('EM011', 'Mert', 'Firat', 'EMP011', 'BR008', 'RL006', 'mert.f', 'pass11', '36000', '2021-12-12', NOW(), 1),
('EM012', 'Ece', 'Uslu', 'EMP012', 'BR009', 'RL004', 'ece.u', 'pass12', '31000', '2023-06-25', NULL, 1),
('EM013', 'Naz', 'Elmas', 'EMP013', 'BR010', 'RL002', 'naz.e', 'pass13', '39000', '2022-10-10', NOW(), 1),
('EM014', 'Bora', 'Ak', 'EMP014', 'BR011', 'RL005', 'bora.a', 'pass14', '28500', '2024-03-01', NOW(), 1),
('EM015', 'Canan', 'Er', 'EMP015', 'BR012', 'RL004', 'canan.e', 'pass15', '32500', '2023-07-15', NOW(), 1);

INSERT INTO Manifests (ManifestID, VehicleID, DestBranchID, OriginBranchID, ArrivalTime, DepartureTime) VALUES
('MN001', 'VH001', 'BR002', 'BR001', '2023-10-27 12:00:00', '2023-10-27 08:00:00'),
('MN002', 'VH004', 'BR004', 'BR001', '2023-10-27 18:00:00', '2023-10-27 09:00:00'),
('MN003', 'VH006', 'BR005', 'BR001', '2023-10-27 16:00:00', '2023-10-27 08:30:00'),
('MN004', 'VH002', 'BR003', 'BR001', '2023-10-27 10:30:00', '2023-10-27 09:30:00'),
('MN005', 'VH008', 'BR001', 'BR006', '2023-10-28 09:00:00', '2023-10-28 06:00:00'),
('MN006', 'VH009', 'BR001', 'BR007', '2023-10-28 20:00:00', '2023-10-28 08:00:00'),
('MN007', 'VH010', 'BR009', 'BR008', '2023-10-27 14:00:00', '2023-10-27 10:00:00'),
('MN008', 'VH005', 'BR011', 'BR004', '2023-10-27 13:00:00', '2023-10-27 10:00:00'),
('MN009', 'VH001', 'BR001', 'BR002', NULL, '2023-10-29 08:00:00'),
('MN010', 'VH012', 'BR001', 'BR010', NULL, '2023-10-29 07:00:00'),
('MN011', 'VH004', 'BR001', 'BR004', NULL, '2023-10-29 22:00:00'),
('MN012', 'VH014', 'BR010', 'BR012', '2023-10-27 15:30:00', '2023-10-27 12:00:00'),
('MN013', 'VH015', 'BR004', 'BR013', '2023-10-27 11:00:00', '2023-10-27 08:00:00'),
('MN014', 'VH011', 'BR008', 'BR009', '2023-10-27 17:00:00', '2023-10-27 14:00:00'),
('MN015', 'VH006', 'BR015', 'BR005', NULL, '2023-10-29 09:00:00');

INSERT INTO Cargos (CargoID, ReceiverCustID, SenderCustID, CargoWeight, CargoLength, CargoWidth, CargoHeight, ShippingCost, OriginBranchID, DestBranchID, CurrentStatus, LastUpdated, PaymentType, PaymentStatus, ServiceTypeID) VALUES
('CG001', 'CU002', 'CU001', 5.50, 20, 30, 15, 120.00, 'BR001', 'BR004', 'Delivered', '2023-10-28 14:00:00', 'Credit Card', 'Paid', 'SV001'),
('CG002', 'CU003', 'CU001', 12.00, 40, 40, 40, 300.00, 'BR001', 'BR005', 'In Transit', '2023-10-29 09:00:00', 'Cash', 'Pending', 'SV002'),
('CG003', 'CU001', 'CU004', 2.00, 10, 15, 5, 80.00, 'BR006', 'BR001', 'Arrived at Branch', '2023-10-28 09:00:00', 'Credit Card', 'Paid', 'SV001'),
('CG004', 'CU005', 'CU002', 0.50, 25, 35, 2, 60.00, 'BR004', 'BR007', 'In Transit', '2023-10-29 08:00:00', 'Sender Pays', 'Paid', 'SV007'),
('CG005', 'CU006', 'CU002', 25.00, 50, 50, 50, 550.00, 'BR004', 'BR008', 'Processing', '2023-10-29 10:00:00', 'Credit Card', 'Paid', 'SV005'),
('CG006', 'CU007', 'CU003', 3.00, 15, 15, 15, 100.00, 'BR005', 'BR001', 'Out for Delivery', '2023-10-29 11:00:00', 'Cash', 'Pending', 'SV003'),
('CG007', 'CU008', 'CU003', 1.00, 10, 10, 10, 75.00, 'BR005', 'BR004', 'Delivered', '2023-10-27 16:00:00', 'Credit Card', 'Paid', 'SV001'),
('CG008', 'CU009', 'CU004', 8.00, 30, 30, 30, 200.00, 'BR006', 'BR005', 'In Transit', '2023-10-29 07:30:00', 'Sender Pays', 'Paid', 'SV001'),
('CG009', 'CU010', 'CU005', 4.00, 20, 20, 20, 150.00, 'BR007', 'BR011', 'Lost', '2023-10-25 10:00:00', 'Credit Card', 'Refunded', 'SV001'),
('CG010', 'CU011', 'CU006', 15.00, 45, 45, 45, 400.00, 'BR008', 'BR010', 'In Transit', '2023-10-29 06:00:00', 'Receiver Pays', 'Pending', 'SV005'),
('CG011', 'CU012', 'CU007', 0.20, 30, 20, 1, 50.00, 'BR001', 'BR012', 'Processing', '2023-10-29 12:00:00', 'Cash', 'Paid', 'SV007'),
('CG012', 'CU013', 'CU008', 6.00, 25, 25, 25, 180.00, 'BR004', 'BR009', 'Delivered', '2023-10-26 14:30:00', 'Credit Card', 'Paid', 'SV002'),
('CG013', 'CU014', 'CU009', 9.00, 35, 35, 35, 220.00, 'BR005', 'BR013', 'In Transit', '2023-10-29 05:00:00', 'Sender Pays', 'Paid', 'SV001'),
('CG014', 'CU015', 'CU010', 50.00, 80, 80, 80, 1200.00, 'BR011', 'BR001', 'Created', '2023-10-29 13:00:00', 'Bank Transfer', 'Paid', 'SV013'),
('CG015', 'CU001', 'CU015', 2.50, 15, 20, 15, 90.00, 'BR015', 'BR001', 'Picked Up', '2023-10-29 11:30:00', 'Cash', 'Pending', 'SV001');

INSERT INTO ManifestCargo (ManifestID, CargoID, LogStatus) VALUES
('MN002', 'CG001', 'Loaded'),
('MN003', 'CG002', 'Loaded'),
('MN005', 'CG003', 'Unloaded'),
('MN002', 'CG004', 'Loaded'),
('MN008', 'CG005', 'Loaded'),
('MN009', 'CG006', 'Loaded'),
('MN003', 'CG007', 'Unloaded'),
('MN015', 'CG008', 'Scheduled'),
('MN006', 'CG009', 'Lost Check'),
('MN007', 'CG010', 'In Transit'),
('MN001', 'CG011', 'Scheduled'),
('MN008', 'CG012', 'Unloaded'),
('MN013', 'CG013', 'Loaded'),
('MN005', 'CG014', 'Scheduled'),
('MN015', 'CG015', 'Scheduled');

INSERT INTO TrackingLog (TrackID, LogTimestamps, CargoID, BranchID, EmployeeID, ReceiverName, ReceiverRelation, StatusID) VALUES
('TR001', '2023-10-27 09:00:00', 'CG001', 'BR001', 'EM001', NULL, NULL, 'ST001'),
('TR002', '2023-10-27 14:00:00', 'CG001', 'BR001', 'EM002', NULL, NULL, 'ST004'),
('TR003', '2023-10-28 09:00:00', 'CG001', 'BR004', 'EM006', NULL, NULL, 'ST008'),
('TR004', '2023-10-28 14:00:00', 'CG001', 'BR004', 'EM007', 'Ayse Demir', 'Self', 'ST010'),
('TR005', '2023-10-29 09:00:00', 'CG002', 'BR001', 'EM001', NULL, NULL, 'ST005'),
('TR006', '2023-10-28 09:00:00', 'CG003', 'BR006', 'EM009', NULL, NULL, 'ST003'),
('TR007', '2023-10-29 08:00:00', 'CG004', 'BR004', 'EM006', NULL, NULL, 'ST005'),
('TR008', '2023-10-29 10:00:00', 'CG005', 'BR004', 'EM007', NULL, NULL, 'ST002'),
('TR009', '2023-10-29 11:00:00', 'CG006', 'BR005', 'EM008', NULL, NULL, 'ST009'),
('TR010', '2023-10-27 16:00:00', 'CG007', 'BR004', 'EM007', 'Selin Koc', 'Self', 'ST010'),
('TR011', '2023-10-29 07:30:00', 'CG008', 'BR006', 'EM009', NULL, NULL, 'ST005'),
('TR012', '2023-10-25 10:00:00', 'CG009', 'BR007', 'EM010', NULL, NULL, 'ST015'),
('TR013', '2023-10-29 06:00:00', 'CG010', 'BR008', 'EM011', NULL, NULL, 'ST005'),
('TR014', '2023-10-29 12:00:00', 'CG011', 'BR001', 'EM001', NULL, NULL, 'ST002'),
('TR015', '2023-10-26 14:30:00', 'CG012', 'BR009', 'EM012', 'Onur Yavuz', 'Self', 'ST010');

INSERT INTO Invoice (InvoiceID, CargoID, CustID, InvoiceDate, TotalAmount) VALUES
('INV01', 'CG001', 'CU001', '2023-10-27 09:05:00', 120.00),
('INV02', 'CG002', 'CU001', '2023-10-29 09:05:00', 300.00),
('INV03', 'CG003', 'CU004', '2023-10-28 09:05:00', 80.00),
('INV04', 'CG004', 'CU002', '2023-10-29 08:05:00', 60.00),
('INV05', 'CG005', 'CU002', '2023-10-29 10:05:00', 550.00),
('INV06', 'CG006', 'CU003', '2023-10-29 11:05:00', 100.00),
('INV07', 'CG007', 'CU003', '2023-10-27 16:05:00', 75.00),
('INV08', 'CG008', 'CU004', '2023-10-29 07:35:00', 200.00),
('INV09', 'CG009', 'CU005', '2023-10-25 10:05:00', 150.00),
('INV10', 'CG010', 'CU006', '2023-10-29 06:05:00', 400.00),
('INV11', 'CG011', 'CU007', '2023-10-29 12:05:00', 50.00),
('INV12', 'CG012', 'CU008', '2023-10-26 14:35:00', 180.00),
('INV13', 'CG013', 'CU009', '2023-10-29 05:05:00', 220.00),
('INV14', 'CG014', 'CU010', '2023-10-29 13:05:00', 1200.00),
('INV15', 'CG015', 'CU015', '2023-10-29 11:35:00', 90.00);