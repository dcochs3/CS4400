INSERT INTO museumDB.admin
VALUES ('admin@gmail.com', 'pass word'),
       ('alex@gatech.edu', 'iamadmin');

INSERT INTO museumDB.visitor
VALUES ('dochs3@gatech.edu', 'cliffdiving', '4123822045026035', 6, 2026, 495, 0),
       ('chall@gatech.edu', 'notapassword', '5674988012346709', 1, 2032, 674, 0),
       ('sweat@gatech.edu', 'adminstaff', '7859456905723245', 5, 2024, 063, 1),       
       ('alex@gatech.edu', 'juststaff', '9635367434680945', 4, 2027, 521, 1),
       ('daniel@gatech.edu', 'bilingual', '1234567812345670', 1, 2020, 123, 0),
       ('helen@gatech.edu', 'architecture4ever', '8765432187654320', 2, 2021, 456, 1),
       ('zoe@gatech.edu', 'yogasister', '2468135924681350', 3, 2022, 789, 1);

INSERT INTO museumDB.museum
VALUES ('Van Gogh Museum', 'sweat@gatech.edu'),
       ('MoA', 'alex@gatech.edu'),
       ('Museum of Illusions', NULL),
       ('MACBA', 'zoe@gatech.edu'),
       ('Picasso Museum', NULL),
       ('CCCB', 'helen@gatech.edu');
              
INSERT INTO museumDB.exhibit
VALUES ('Van Gogh Museum', 'bird', 1983, NULL, 'sweat@gatech.edu'),
       ('Van Gogh Museum', 'plane', 1990, NULL, 'sweat@gatech.edu'),
       ('Van Gogh Museum', 'superman', 1995, NULL, 'sweat@gatech.edu'),
       ('MoA', 'crying college student', 1995, NULL, 'alex@gatech.edu'),
       ('MACBA', 'Bird', 2018, 'www.macba.es/bird/', 'zoe@gatech.edu'),
       ('MACBA', 'Plane', 2018, 'www.macba.es/plane/', 'zoe@gatech.edu'),
       ('MACBA', 'Train', 2018, 'www.macba.es/train/', 'zoe@gatech.edu'),
       ('Picasso Museum', 'Geometric Shapes', 1900, 'www.picassomuseo.com/geo/', NULL),
       ('CCCB', 'Black Light 1', 1985, 'www.cccb.com/bl1', 'helen@gatech.edu'),
       ('CCCB', 'Black Light 2', 1986, 'www.cccb.com/bl2', 'helen@gatech.edu');

INSERT INTO museumDB.ticket
VALUES ('MoA', 'chall@gatech.edu', 5, '2018-05-20'),
       ('Van Gogh Museum', 'chall@gatech.edu', 20, '2018-06-01'),
       ('Van Gogh Museum', 'dochs3@gatech.edu', 10, '2018-06-10'),
       ('MACBA', 'zoe@gatech.edu', 5, '2018-05-20'),
       ('Picasso Museum', 'helen@gatech.edu', 20, '2018-06-11'),
       ('CCCB', 'helen@gatech.edu', 50, '2018-06-29');

INSERT INTO museumDB.review
VALUES ('Van Gogh Museum', 'alex@gatech.edu', 'Decent', 4),
       ('Museum of Illusions', 'chall@gatech.edu', 'Wild!', 5),
       ('MACBA', 'zoe@gatech.edu', 'Didn\'t get it.', 1),
       ('Picasso Museum', 'helen@gatech.edu', 'So many shapes!', 5),
       ('CCCB', 'helen@gatech.edu', 'Scary, but cool', 3);


INSERT INTO museumDB.curator_request
values ('Museum of Illusions', 'dochs3@gatech.edu'),
       ('Museum of Illusions', 'chall@gatech.edu'),
       ('Picasso Museum', 'zoe@gatech.edu');