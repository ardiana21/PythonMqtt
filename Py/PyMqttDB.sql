/*
MariaDB Backup
Database: python
Backup Time: 2022-03-11 16:28:16
*/

SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS `python`.`cards`;
DROP TABLE IF EXISTS `python`.`devices`;
DROP TABLE IF EXISTS `python`.`logs`;
CREATE TABLE `cards` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `cardUid` varchar(20) NOT NULL,
  `cardStatus` enum('enable','disable') NOT NULL DEFAULT 'disable',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `deviceName` varchar(50) NOT NULL,
  `deviceID` varchar(20) NOT NULL,
  `registerDate` date NOT NULL,
  `deviceMode` enum('enable','disable') DEFAULT 'disable',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `deviceId` varchar(20) NOT NULL,
  `cardUid` varchar(20) NOT NULL,
  `checkInDate` date NOT NULL,
  `timeIn` time NOT NULL DEFAULT current_timestamp(),
  `timeOut` time NOT NULL DEFAULT '00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;
BEGIN;
LOCK TABLES `python`.`cards` WRITE;
DELETE FROM `python`.`cards`;
INSERT INTO `python`.`cards` (`id`,`username`,`cardUid`,`cardStatus`) VALUES (1, 'aaa', '12345678', 'enable'),(2, 'bbb', '11111111', 'disable');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `python`.`devices` WRITE;
DELETE FROM `python`.`devices`;
INSERT INTO `python`.`devices` (`id`,`deviceName`,`deviceID`,`registerDate`,`deviceMode`) VALUES (1, 'Reader1', '001', '2022-02-11', 'enable'),(2, 'Reader2', '002', '2022-02-11', 'disable'),(3, 'Register1', '003', '2022-02-11', 'disable');
UNLOCK TABLES;
COMMIT;
BEGIN;
LOCK TABLES `python`.`logs` WRITE;
DELETE FROM `python`.`logs`;
INSERT INTO `python`.`logs` (`id`,`username`,`deviceId`,`cardUid`,`checkInDate`,`timeIn`,`timeOut`) VALUES (15, 'aaa', '001', '12345678', '2022-03-11', '16:20:58', '00:00:00');
UNLOCK TABLES;
COMMIT;
