-- Database: `electricity_bill`
-- Create the database
CREATE DATABASE IF NOT EXISTS `electricity_bill`;
USE `electricity_bill`;

-- Table: `customer`
-- Create the `customer` table
CREATE TABLE IF NOT EXISTS `customer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `meterno` int(250) NOT NULL,
  `consumerno` bigint(250) NOT NULL,
  `consumername` varchar(250) NOT NULL,
  `load_con` varchar(5) NOT NULL DEFAULT '5',
  `unit_consumed` int(250) NOT NULL,
  `month` varchar(20) NOT NULL,
  `year` int(4) NOT NULL DEFAULT current_timestamp(),
  `email` varchar(250) NOT NULL,
  `address` text NOT NULL,
  `amountgen` decimal(11,5) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: `dept`
-- Create the `dept` table
CREATE TABLE IF NOT EXISTS `dept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dept_no` int(20) NOT NULL,
  `deptname` varchar(500) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `deptname` (`deptname`),
  UNIQUE KEY `dept_no` (`dept_no`),
  UNIQUE KEY `dept_unique` (`deptname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert data into the `dept` table
INSERT IGNORE INTO `dept` (`dept_no`, `deptname`) VALUES
(156758, 'ADMIN'),
(145759, 'BILL GENERATION'),
(145761, 'BILL DELIVERY'),
(15675812, 'CUSTOMER');

-- Table: `login`
-- Create the `login` table
CREATE TABLE IF NOT EXISTS `login` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` varchar(250) NOT NULL,
  `branch` varchar(500) NOT NULL,
  `session_in` datetime NOT NULL DEFAULT current_timestamp(),
  `session_out` datetime NOT NULL,
  `dept_no` int(20) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `branch` (`branch`),
  KEY `userid` (`userid`),
  KEY `login_ibfk_3` (`dept_no`),
  CONSTRAINT `login_ibfk_1` FOREIGN KEY (`branch`) REFERENCES `user` (`useradmin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `login_ibfk_2` FOREIGN KEY (`userid`) REFERENCES `user` (`useradmin_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `login_ibfk_3` FOREIGN KEY (`dept_no`) REFERENCES `user` (`dept_no`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(250) NOT NULL,
  `password` varchar(100) NOT NULL,
  `branch` varchar(500) NOT NULL,
  `dept_no` int(20) NOT NULL,
  `useradmin_id` varchar(250) NOT NULL COMMENT 'This is the user id',
  PRIMARY KEY (`id`),
  UNIQUE KEY `useradmin_id` (`useradmin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;