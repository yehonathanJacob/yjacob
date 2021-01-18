INSERT INTO Product (code, pname, descr, utype, uprice, manu, sid) VALUES
        (987, 'Tomatoes',       'Vegetable',  'Kg',  5.99,  'manufacturer1', 111),
        (876, 'Cucumbers',      'Vegetable',  'Kg',  4.99,  'manufacturer2', 222),
        (765, 'Cornflakes',     'Cornflakes', 'Box', 15.9,  'manufacturer2', 222),
        (654, 'Camembert',      'Cheese',     'Box', 12.50, 'manufacturer2', 111),
        (543, 'sweet potato',   'Vegetable',  'Kg',  16.40, 'manufacturer3', 333),
        (432, 'red pepper',     'Vegetable',  'Kg',  15.99, 'manufacturer1', 111);

insert info product (code, pname, descr, utype, uprice, manu, sid) values
        (101, 'prod1 n',  'description 1',  'kilo',  1.99, 'manufacturer 1', 201),
		(102, 'prod2 n',  'description 1',  'liter', 2.47, 'manufacturer 1', 202),
        (103, 'prod3 n',  'description 2',  'kilo',   5.0, 'manufacturer 2', 202),
        (104, 'prod4 n',  'description 3',  'liter',  4.5, 'manufacturer 1', 201),
        (105, 'prod5 n',  'description 3',  'liter',  4.5, 'manufacturer 1', 201),
        (106, 'prod6 n',  'description 3',  'liter',16.40, 'manufacturer 3', 203);  


INSERT INTO Branch (bid, bname, baddress) VALUES
        (989, 'tal aviv', 'road 1 tel aviv'),
        (878, 'Raanana',  'road 1 raanana'),
        (767, 'Holon',    'road 1 holon');

INSERT INTO Supplier (sid, sname, address, phone) VALUES
        (111, 'supplier2', 'road2 tel aviv',  111111111),
        (222, 'supplier3', 'road3 jerusalem', 222222222),
        (333, 'supplier4', 'road2 eilat',     333333333);
 
INSERT INTO Stock (code, bid, units) VALUES
        (987, 989, 50),
        (987, 878, 75),
        (987, 767, 100),
        (876, 989, 30),
        (876, 878, 60),
        (876, 767, 25),
        (765, 989, 20),
        (765, 878, 15),
        (654, 878, 10),
        (654, 767, 5),
        (543, 989, 50),
        (543, 767, 165),
        (432, 989, 17),
        (432, 878, 25),
        (432, 767, 30);
 
INSERT INTO Receipt (bid, rdate, rtime, ptype) VALUES
        (989, '2020-3-18', '10:00', 'Cash'),
        (989, '2020-7-16', '12:30', 'Credit'),
        (989, '2020-7-15', '15:35', 'Credit'),
        (878, '2020-3-17', '8:30',  'Cash'),
        (878, '2020-7-22', '7:00',  'Credit'),
        (767, '2020-7-13', '22:00', 'Cash'),
        (767, '2020-3-10', '20:30', 'Cash'),
        (767, '2020-5-14', '14:25', 'Credit');
 
 
INSERT INTO Purchase (bid, rdate, rtime, code, units) VALUES
        (989, '2020-3-18', '10:00', 987, 5),
        (989, '2020-3-18', '10:00', 876, 3),
        (989, '2020-3-18', '10:00', 543, 4),
        (989, '2020-3-18', '10:00', 432, 1),
        (878, '2020-3-17', '8:30',  654, 1),
        (878, '2020-3-17', '8:30',  432, 3),
        (767, '2020-3-10', '20:30', 654, 2),
        (767, '2020-3-10', '20:30', 987, 3);