create table Product(
code int,
 pname varchar(30),
 descr varchar(50),
 utype varchar(30),
 uprice float,
 manu varchar(30),
 sid int,
primary key (code));

create table Branch(
bid int,
 bname varchar(30),
 baddress varchar(50),
primary key (bid));

create table Supplier(
sid int,
 sname varchar(30),
 address varchar(50),
 phone varchar(30),
primary key (sid));

create table Stock(
code int,
 bid int,
 units float,
primary key (code, bid),
Foreign key (code) references Product (code),
Foreign key (bid) references Branch (bid));

create table Receipt(
bid int,
 rdate date,
 rtime time,
 ptype varchar(30),
 total float default 0,
primary key (bid, rdate, rtime),
Foreign key (bid) references Branch (bid));

create table Purchase(
 bid int,
 rdate date,
 rtime time,
 code int,
 units float check(units>0),
primary key (bid, rdate, rtime, code),
Foreign key (bid, rdate, rtime) references Receipt (bid, rdate, rtime),
Foreign key (code) references Product (code));