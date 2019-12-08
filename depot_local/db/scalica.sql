/* Create our database */
CREATE DATABASE IF NOT EXISTS scalica CHARACTER SET utf8;

/* Setup permissions for the server */
CREATE USER IF NOT EXISTS 'appserver'@'localhost' IDENTIFIED BY 'foobarzoot';
CREATE USER IF NOT EXISTS 'www-data'@'localhost' IDENTIFIED BY 'foobarzoot';
GRANT ALL ON scalica.* TO 'appserver'@'localhost';
GRANT ALL ON scalica.* TO 'www-data'@'localhost';
