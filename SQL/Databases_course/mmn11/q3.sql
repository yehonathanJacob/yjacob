insert into product (code, pname, descr, utype, uprice, manu, sid) values
        (101, 'prod1 n',  'description 1',  'kilo',  1.99, 'manufacturer 1', 201),
		(102, 'prod2 n',  'description 1',  'liter',12.47, 'manufacturer 2', 202),
        (103, 'prod3 n',  'description 2',  'kilo',   5.0, 'manufacturer 2', 202),
        (104, 'prod4 n',  'description 3',  'liter',  4.5, 'manufacturer 1', 201),
        (105, 'prod5 n',  'description 3',  'liter',  4.5, 'manufacturer 1', 201),
        (106, 'prod6 n',  'description 3',  'kilo' ,16.40, 'manufacturer 3', 203);  

insert into branch (bid, bname, baddress) values
        (301, 'Tell Aviv', 'Begin 1 Tell Aviv'),
        (302, 'Jerusalem',  'Jabutinski 2 Jerusalem'),
        (303, 'Haifa',    'Dizingof 3 Haifa');
		
insert into supplier (sid, sname, address, phone) values
        (201, 'supplier 1', 'Begin 4 Tell Aviv',      '050-010-1010'),
        (202, 'supplier 2', 'Jabutinski 7 Jerusalem', '050-020-2020'),
        (203, 'supplier 3', 'Hertzel 3 Haifa',        '050-030-3030'); 
 
insert into stock (code, bid, units) values
        (101, 301, 50),
        (101, 302, 75),
        (101, 303, 100),
        (102, 301, 30),
        (102, 302, 60),
        (102, 303, 25),
        (103, 301, 20),
        (103, 302, 15),
        (104, 302, 10),
        (104, 303, 5),
        (105, 301, 50),
        (105, 303, 165),
        (106, 301, 17),
        (106, 302, 25),
		(105, 302, 10),
        (106, 303, 30);
 
insert into receipt (bid, rdate, rtime, ptype) values
		(301, '2020-08-18', '08:00', 'Cash'),
        (301, '2020-08-28', '10:30', 'Cash'),
        (301, '2020-07-26', '12:30', 'Credit'),
        (301, '2020-05-06', '15:35', 'Credit'),
        (302, '2020-04-17', '8:30',  'Cash'),
        (302, '2020-06-22', '7:00',  'Credit'),
        (303, '2020-02-13', '22:00', 'Cash'),
        (303, '2019-08-10', '20:30', 'Cash'),
        (303, '2020-05-12', '14:25', 'Credit');
 
insert into purchase (bid, rdate, rtime, code, units) values
        (301, '2020-08-18', '08:00', 101, 5),
        (301, '2020-08-28', '10:30', 102, 3),
        (301, '2020-08-18', '08:00', 105, 4),
        (301, '2020-08-18', '08:00', 106, 1),
        (302, '2020-04-17', '8:30',  104, 1),
        (302, '2020-04-17', '8:30',  106, 3),
        (303, '2019-08-10', '20:30', 104, 2),
        (303, '2019-08-10', '20:30', 101, 3);