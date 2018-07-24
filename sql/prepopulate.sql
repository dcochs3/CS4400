INSERT INTO museumDB.admin
VALUES ('admin@gmail.com', 'pass word');

INSERT INTO museumDB.visitor
VALUES ('dochs3@gatech.edu', 'cliffdiving', '4123822045026035', 6, 2026, 495, 0),
       ('chall@gatech.edu', 'notapassword', '5674988012346709', 1, 2032, 674, 0),
       ('sweat@gatech.edu', 'adminstaff', '7859456905723245', 5, 2024, 063, 1),       
       ('alex@gatech.edu', 'juststaff', '9635367434680945', 4, 2027, 521, 1);

INSERT INTO museumDB.museum
VALUES ('Picasso Museum', 'sweat@gatech.edu'),
       ('MACBA', 'alex@gatech.edu'),
       ('Museum of Illusions', NULL);
              
INSERT INTO museumDB.exhibit
VALUES ('Picasso Museum', 'bird', 1983, NULL, 'sweat@gatech.edu')
('Picasso Museum', 'plane', 1990, NULL, 'sweat@gatech.edu')
('Picasso Museum', 'superman', 1995, NULL, 'sweat@gatech.edu')
('MACBA', 'crying college student', 1995, NULL, 'alex@gatech.edu');

INSERT INTO museumDB.ticket
VALUES ('chall@gatech.edu', 'MACBA', 5, 2018-05-20)
('chall@gatech.edu', 'Picasso Museum', 20, 2018-06-01)
('dochs3@gatech.edu', 'Picasso Museum', 10, 2018-06-10);

INSERT INTO museumDB.review
VALUES ('Picasso Museum', 'alex@gatech.edu', 'Decent', 4)
('Museum of Illusions', 'chall@gatech.edu', 'Wild!', 5);

INSERT INTO museumDB.curator_request
values ('Museum of Illusions', 'dochs3@gatech.edu'),
       ('Museum of Illusions', 'chall@gatech.edu');