-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: sql3.freesqldatabase.com
-- Generation Time: Oct 21, 2017 at 12:58 PM
-- Server version: 5.5.49-0ubuntu0.12.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sql3181859`
--
CREATE DATABASE IF NOT EXISTS `sql3181859` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `sql3181859`;

-- --------------------------------------------------------

--
-- Table structure for table `bunks`
--

CREATE TABLE `bunks` (
  `shelterIdFk` int(16) UNSIGNED NOT NULL DEFAULT '0',
  `maleCount` int(16) UNSIGNED DEFAULT '0',
  `femaleCount` int(16) UNSIGNED DEFAULT '0',
  `mixedCount` int(16) UNSIGNED DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bunks`
--

INSERT INTO `bunks` (`shelterIdFk`, `maleCount`, `femaleCount`, `mixedCount`) VALUES
(3, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `catId` int(16) UNSIGNED NOT NULL,
  `category` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`catId`, `category`) VALUES
(1, 'Food'),
(2, 'Supplies');

-- --------------------------------------------------------

--
-- Table structure for table `clientLogs`
--

CREATE TABLE `clientLogs` (
  `clientLogId` int(16) UNSIGNED NOT NULL,
  `clientIdFk` int(16) UNSIGNED DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `siteIdFk` int(16) UNSIGNED DEFAULT NULL,
  `textNotes` varchar(255) DEFAULT NULL,
  `logType` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clientLogs`
--

INSERT INTO `clientLogs` (`clientLogId`, `clientIdFk`, `time`, `siteIdFk`, `textNotes`, `logType`) VALUES
(33, 1, '2017-07-30 03:05:48', NULL, 'Description modified: Driver License: 13579474(original: ID: 1234567 ). ', 'modified'),
(34, 1, '2017-07-30 03:06:05', NULL, 'Phone modified: (405) 222-333(original: 1234567890 ). ', 'modified'),
(35, 1, '2017-07-30 03:06:43', 1, 'Service used: Food Pantry; Notes: Take foods to home', 'checkin'),
(36, 2, '2017-07-30 03:07:57', NULL, 'Description modified: SSN 1234(original: Female ). ', 'modified'),
(37, 2, '2017-07-30 03:08:14', NULL, 'Description modified: DL 123456(original: SSN 1234 ). ', 'modified'),
(38, 2, '2017-07-30 03:09:00', 1, 'Service used: Food Pantry; Notes: Take some beef', 'checkin'),
(39, 3, '2017-07-30 03:09:52', NULL, 'Phone modified: 4891234567(original: (123)456-7890 ). ', 'modified'),
(40, 3, '2017-07-30 03:10:24', 1, 'Service used: Food Pantry; Notes: Does no eat pork', 'checkin'),
(41, 3, '2017-07-30 03:12:22', 1, 'Service used: Food Pantry; Notes: Allergy to peanuts', 'checkin'),
(42, 4, '2017-07-30 03:13:13', NULL, 'Description modified: DL 543678(original: ssn 12345678 ). ', 'modified'),
(43, 4, '2017-07-30 03:13:49', 1, 'Service used: Food Pantry; Notes: Take some food for his brother', 'checkin'),
(44, 4, '2017-07-30 03:14:37', 1, 'Service used: Notes: Do nothing because shelter is not available at this site.', 'checkin'),
(45, 5, '2017-07-30 03:15:45', NULL, 'Description modified: DL 0987654(original: ssn 12345678 ). ', 'modified'),
(46, 5, '2017-07-30 03:16:10', 2, 'Service used: Soup Kitchen; shelter; Notes: ', 'checkin'),
(47, 5, '2017-07-30 03:16:53', 2, 'Service used: Soup Kitchen; Notes: Allergy to beans', 'checkin'),
(48, 6, '2017-07-30 03:18:11', NULL, 'Description modified: Female(original: Male ). ', 'modified'),
(49, 6, '2017-07-30 03:18:28', NULL, 'Phone modified: (405) 222-4444(original: 1234567890 ). ', 'modified'),
(50, 6, '2017-07-30 03:19:06', 2, 'Service used: Soup Kitchen; Notes: Like to eat beef', 'checkin'),
(51, 7, '2017-07-30 03:19:42', NULL, 'Description modified: SSN 09876(original: ssn 000 ). ', 'modified'),
(52, 7, '2017-07-30 03:20:01', NULL, 'Phone modified: 12457802(original: 7654321098 ). ', 'modified'),
(53, 7, '2017-07-30 03:20:28', 2, 'Service used: Soup Kitchen; shelter; Notes: Allergy to beef', 'checkin'),
(54, 8, '2017-07-30 03:23:09', NULL, 'Description modified: dl 45678(original: dl 12345 ). ', 'modified'),
(55, 8, '2017-07-30 03:23:25', 2, 'Service used: Soup Kitchen; shelter; Notes: ', 'checkin'),
(56, 8, '2017-07-30 03:23:55', 2, 'Service used: Notes: Do nothing because shelter is not available at this site.', 'checkin'),
(57, 9, '2017-07-30 03:24:50', NULL, 'Phone modified: 1234567890(original: 0000000000 ). ', 'modified'),
(58, 9, '2017-07-30 03:25:06', NULL, 'Description modified: SSN 567890(original: DL 24680 ). ', 'modified'),
(59, 9, '2017-07-30 03:25:34', 3, 'Service used: Food Pantry; Notes: Take some beef', 'checkin'),
(60, 10, '2017-07-30 03:26:13', NULL, 'Description modified: Driver License: 23456(original: Drive license: 1234567 ). ', 'modified'),
(61, 10, '2017-07-30 03:26:23', 3, 'Service used: Food Pantry; Soup Kitchen; shelter; Notes: ', 'checkin'),
(62, 10, '2017-07-30 03:26:43', 3, 'Service used: Soup Kitchen; Notes: Have dinner here', 'checkin'),
(63, 11, '2017-07-30 03:27:37', NULL, 'Description modified: SSN 1234(original: SSN 4321 ). ', 'modified'),
(64, 11, '2017-07-30 03:27:47', NULL, 'Phone modified: (405) 222-333(original: 9876543210 ). ', 'modified'),
(65, 11, '2017-07-30 03:28:29', 3, 'Service used: Food Pantry; Soup Kitchen; shelter; Notes: Come here with a boy', 'checkin'),
(66, 12, '2017-07-30 03:29:15', NULL, 'Phone modified: 12457802(original: (405) 222-333 ). ', 'modified'),
(67, 12, '2017-07-30 03:29:39', 3, 'Service used: Notes: Did nothing', 'checkin'),
(68, 12, '2017-07-30 03:30:06', 3, 'Service used: Food Pantry; Notes: Take 2 sandwishes away', 'checkin'),
(82, 18, '2017-07-30 16:28:13', NULL, 'Description modified: Driver License: 135794(original: SSN 1234 ). Phone modified: 2222(original: 111111 ). ', 'modified'),
(83, 18, '2017-07-30 16:28:57', 1, 'Service used: Soup Kitchen; Notes: ', 'checkin'),
(84, 1, '2017-07-30 16:30:28', 1, 'Service used: Food Pantry; Soup Kitchen; shelter; Notes: ', 'checkin');

-- --------------------------------------------------------

--
-- Table structure for table `clients`
--

CREATE TABLE `clients` (
  `clientId` int(16) UNSIGNED NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `phone` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `clients`
--

INSERT INTO `clients` (`clientId`, `fullName`, `description`, `phone`) VALUES
(1, 'Joe Client1', 'ssn 000', '(405) 222-333'),
(2, 'Joe Client2', 'DL 123456', '2015874562'),
(3, 'Joe Client3', 'Drive license: 1234567', '4891234567'),
(4, 'Joe Client4', 'DL 543678', '1234567890'),
(5, 'Joe Client5', 'DL 0987654', '1234567890'),
(6, 'Joe Client6', 'Female', '(405) 222-4444'),
(7, 'Jane Client7', 'SSN 09876', '12457802'),
(8, 'Jane Client8', 'dl 45678', '123-4567'),
(9, 'Jane Client9', 'SSN 567890', '1234567890'),
(10, 'Jane Client10', 'Driver License: 23456', '(123)456-7890'),
(11, 'Jane Client11', 'SSN 1234', '(405) 222-333'),
(12, 'Jane Client12', 'Driver License: 13579474', '12457802'),
(18, 'Eric z', 'Driver License: 135794', '2222');

-- --------------------------------------------------------

--
-- Table structure for table `foodBanks`
--

CREATE TABLE `foodBanks` (
  `foodBankId` int(16) UNSIGNED NOT NULL,
  `siteIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `foodBanks`
--

INSERT INTO `foodBanks` (`foodBankId`, `siteIdFk`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- --------------------------------------------------------

--
-- Table structure for table `foodPantries`
--

CREATE TABLE `foodPantries` (
  `foodPantryId` int(16) UNSIGNED NOT NULL,
  `description` varchar(255) NOT NULL,
  `hours` varchar(255) NOT NULL,
  `conditions` varchar(255) NOT NULL,
  `siteIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `foodPantries`
--

INSERT INTO `foodPantries` (`foodPantryId`, `description`, `hours`, `conditions`, `siteIdFk`) VALUES
(1, 'pantry 1', '6am-6pm', 'ssn', 1),
(3, 'pantry3', '7/24', 'Photo Id', 3);

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `itemId` int(16) UNSIGNED NOT NULL,
  `item` varchar(255) NOT NULL,
  `subCatIdFk` int(16) UNSIGNED NOT NULL,
  `storageIdFk` int(16) UNSIGNED NOT NULL,
  `quantity` int(16) UNSIGNED NOT NULL,
  `expiration` datetime DEFAULT '2099-01-01 00:00:00',
  `foodBankIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`itemId`, `item`, `subCatIdFk`, `storageIdFk`, `quantity`, `expiration`, `foodBankIdFk`) VALUES
(1, 'leafy vegetable 1', 1, 2, 40, '2017-08-11 00:00:00', 1),
(2, 'leafy vegetable 1', 1, 2, 20, '2017-08-01 00:00:00', 1),
(3, 'walnuts', 1, 2, 68, '2017-11-30 00:00:00', 1),
(4, 'peanuts', 2, 1, 15, '2017-09-29 00:00:00', 1),
(5, 'soda drinks', 6, 2, 20, '2017-12-31 00:00:00', 1),
(6, 'pop drinks', 6, 2, 14, '2017-12-31 00:00:00', 1),
(7, 'red meat-beef', 3, 3, 5, '2017-08-31 00:00:00', 1),
(8, 'red meat-pork', 3, 3, 24, '2017-09-01 00:00:00', 1),
(9, 'swiss cheese', 4, 2, 20, '2017-08-31 00:00:00', 1),
(10, 'frech cheese', 4, 2, 0, '2017-12-31 00:00:00', 1),
(11, 'toothbrush', 7, 1, 8, '2099-01-01 00:00:00', 1),
(13, 'baby wipes', 7, 1, 24, '2019-07-31 00:00:00', 1),
(14, 'shampoo', 7, 1, 20, '2019-07-31 00:00:00', 1),
(15, 'soap', 7, 1, 5, '2018-05-31 00:00:00', 1),
(16, 'root veggie-radish', 1, 2, 10, '2017-08-31 00:00:00', 2),
(17, 'root veggie-potato', 1, 2, 10, '2017-09-30 00:00:00', 2),
(18, 'grains-rice', 2, 1, 10, '2018-08-31 00:00:00', 2),
(19, 'grains-corn', 2, 1, 8, '2018-09-30 00:00:00', 2),
(20, 'tomato sauce', 5, 1, 8, '2018-01-31 00:00:00', 2),
(21, 'grill sauce', 5, 1, 10, '2018-04-30 00:00:00', 2),
(22, 'apple juice', 6, 2, 48, '2018-01-31 00:00:00', 2),
(23, 'orange juice', 6, 2, 36, '2018-04-30 00:00:00', 2),
(24, 'seafood-catfish', 3, 3, 30, '2017-10-31 00:00:00', 2),
(25, 'seafood-shrimp', 3, 3, 30, '2018-01-01 00:00:00', 2),
(26, 'duck eggs', 4, 2, 100, '2017-10-31 00:00:00', 2),
(27, 'chicken eggs', 4, 2, 300, '2017-10-01 00:00:00', 2),
(28, 'tent', 9, 1, 4, '2099-01-01 00:00:00', 2),
(29, 'sleeping bags', 9, 1, 8, '2099-01-01 00:00:00', 2),
(30, 'blankets', 9, 1, 50, '2099-01-01 00:00:00', 2),
(31, 'winter jackets', 9, 1, 15, '2099-01-01 00:00:00', 2),
(32, 'rain coat', 9, 1, 25, '2099-01-01 00:00:00', 2),
(33, 'paper products', 10, 1, 21, '2099-01-01 00:00:00', 2),
(34, 'batteries', 10, 1, 100, '2099-01-01 00:00:00', 2),
(35, 'toilet paper', 10, 1, 22, '2099-01-01 00:00:00', 2),
(36, 'books', 10, 1, 50, '2099-01-01 00:00:00', 2),
(37, 'pet food', 10, 1, 100, '2018-10-01 00:00:00', 2),
(38, 'expired chicken', 3, 2, 12, '2017-05-31 00:00:00', 3),
(47, 'expired chicken meat', 3, 2, 24, '2017-03-31 00:00:00', 3),
(48, 'expired whole milk', 4, 2, 18, '2017-05-31 00:00:00', 3),
(49, 'expired fat free milk', 4, 2, 10, '2017-06-30 00:00:00', 3),
(50, 'shirts', 8, 1, 0, '2099-01-01 00:00:00', 1),
(51, 'pants', 8, 1, 48, '2099-01-01 00:00:00', 1),
(52, 'underwear', 8, 1, 20, '2099-01-01 00:00:00', 1),
(53, 'skirt', 8, 1, 8, '2099-01-01 00:00:00', 1),
(54, 'hat', 8, 1, 20, '2099-01-01 00:00:00', 1),
(69, 'apple-to delete', 1, 2, 12, '2017-09-29 00:00:00', 1),
(70, 'orange-to delete', 1, 2, 12, '2017-08-23 00:00:00', 1),
(76, 'eggplants111', 1, 2, 10, '2017-07-31 00:00:00', 1),
(77, 'random itm', 7, 2, 12, '2099-01-01 00:00:00', 3);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `requestId` int(16) UNSIGNED NOT NULL,
  `requestedQty` int(16) NOT NULL,
  `providedQty` int(16) NOT NULL DEFAULT '0',
  `status` varchar(20) NOT NULL,
  `makingUserFk` int(16) UNSIGNED NOT NULL,
  `approvingUserFk` int(16) UNSIGNED DEFAULT NULL,
  `itemIdFk` int(16) UNSIGNED NOT NULL,
  `foodBankIdFk` int(16) UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`requestId`, `requestedQty`, `providedQty`, `status`, `makingUserFk`, `approvingUserFk`, `itemIdFk`, `foodBankIdFk`) VALUES
(29, 5, 5, 'closed', 3, 1, 4, 1),
(30, 20, 15, 'partial', 3, 1, 3, 1),
(31, 3, 0, 'pending', 3, NULL, 16, 2),
(32, 3, 0, 'pending', 3, NULL, 19, 2),
(34, 4, 0, 'out of stock', 3, NULL, 10, 1),
(35, 2, 1, 'out of stock', 3, 1, 50, 1),
(36, 2, 0, 'pending', 3, NULL, 53, 1),
(37, 10, 0, 'pending', 3, NULL, 30, 2),
(38, 3, 0, 'pending', 3, NULL, 31, 2),
(39, 5, 0, 'pending', 3, NULL, 51, 1),
(40, 5, 0, 'pending', 3, NULL, 32, 2),
(41, 5, 0, 'pending', 2, NULL, 4, 1),
(42, 1, 0, 'pending', 2, NULL, 7, 1),
(43, 3, 2, 'partial', 2, 6, 48, 3),
(44, 2, 0, 'pending', 2, NULL, 38, 3),
(45, 5, 0, 'pending', 2, NULL, 9, 1),
(46, 2, 0, 'pending', 2, NULL, 8, 1),
(47, 4, 0, 'pending', 2, NULL, 13, 1),
(48, 5, 0, 'pending', 2, NULL, 52, 1),
(49, 2, 0, 'pending', 2, NULL, 11, 1),
(50, 2, 0, 'pending', 1, NULL, 18, 2),
(51, 10, 0, 'pending', 1, NULL, 26, 2),
(52, 7, 0, 'pending', 1, NULL, 24, 2),
(53, 3, 0, 'pending', 1, NULL, 47, 3),
(54, 2, 0, 'pending', 1, NULL, 38, 3),
(55, 5, 5, 'closed', 1, 2, 30, 2),
(56, 5, 3, 'partial', 1, 2, 35, 2),
(57, 5, 2, 'partial', 2, 1, 51, 1),
(58, 4, 4, 'closed', 2, 1, 14, 1),
(59, 2, 2, 'closed', 3, 1, 11, 1),
(60, 2, 2, 'closed', 3, 2, 20, 2),
(61, 3, 0, 'pending', 4, NULL, 17, 2),
(62, 12, 0, 'pending', 4, NULL, 26, 2),
(63, 4, 0, 'pending', 4, NULL, 24, 2),
(64, 10, 0, 'pending', 4, NULL, 34, 2),
(65, 1, 0, 'pending', 4, NULL, 29, 2),
(66, 5, 4, 'partial', 4, 5, 33, 2),
(67, 2, 2, 'closed', 4, 5, 19, 2),
(68, 3, 0, 'pending', 5, NULL, 8, 1),
(69, 5, 0, 'pending', 5, NULL, 1, 1),
(70, 6, 0, 'pending', 5, NULL, 5, 1),
(71, 5, 0, 'pending', 5, NULL, 2, 1),
(72, 3, 0, 'pending', 5, NULL, 54, 1),
(73, 1, 0, 'pending', 5, NULL, 15, 1),
(74, 1, 0, 'pending', 5, NULL, 14, 1),
(75, 2, 0, 'pending', 5, NULL, 48, 3),
(76, 2, 0, 'pending', 5, NULL, 38, 3),
(77, 1, 1, 'out of stock', 5, 4, 50, 1),
(78, 12, 12, 'closed', 5, 4, 3, 1),
(79, 3, 0, 'pending', 4, NULL, 48, 3),
(80, 2, 0, 'pending', 4, NULL, 49, 3),
(81, 3, 0, 'pending', 6, NULL, 1, 1),
(82, 4, 0, 'pending', 6, NULL, 8, 1),
(83, 7, 0, 'pending', 6, NULL, 5, 1),
(84, 3, 0, 'out of stock', 6, NULL, 10, 1),
(86, 1, 0, 'pending', 6, NULL, 54, 1),
(87, 3, 0, 'pending', 6, NULL, 14, 1),
(88, 3, 0, 'pending', 6, NULL, 33, 2),
(89, 3, 0, 'pending', 6, NULL, 31, 2),
(90, 3, 0, 'pending', 6, NULL, 35, 2),
(91, 4, 0, 'pending', 6, NULL, 17, 2),
(92, 3, 0, 'pending', 6, NULL, 27, 2),
(93, 5, 5, 'closed', 6, 4, 3, 1),
(94, 5, 5, 'closed', 6, 5, 30, 2),
(95, 5, 0, 'pending', 2, NULL, 70, 1),
(96, 5, 0, 'pending', 2, NULL, 69, 1);

-- --------------------------------------------------------

--
-- Table structure for table `shelters`
--

CREATE TABLE `shelters` (
  `shelterId` int(16) UNSIGNED NOT NULL,
  `description` varchar(255) NOT NULL,
  `hours` varchar(255) NOT NULL,
  `conditions` varchar(255) NOT NULL,
  `siteIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `shelters`
--

INSERT INTO `shelters` (`shelterId`, `description`, `hours`, `conditions`, `siteIdFk`) VALUES
(3, 'shelter3', '8:00am-8:00pm', 'Photo ID', 3);

-- --------------------------------------------------------

--
-- Table structure for table `sites`
--

CREATE TABLE `sites` (
  `siteId` int(16) UNSIGNED NOT NULL,
  `siteName` varchar(20) NOT NULL,
  `street` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `state` varchar(10) NOT NULL,
  `zip` varchar(10) NOT NULL,
  `phone` bigint(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sites`
--

INSERT INTO `sites` (`siteId`, `siteName`, `street`, `city`, `state`, `zip`, `phone`) VALUES
(1, 'site1', '3538 Harter Street', 'Atlanta', 'GA', '30346', 6783468751),
(2, 'site2', '296 Hiddenview Drive', 'ATLANTA', 'GA', '30340', 3424567231),
(3, 'site3', '4543 Layman Court', 'LONDON', 'GA', '72847', 3422317631);

-- --------------------------------------------------------

--
-- Table structure for table `soupKitchens`
--

CREATE TABLE `soupKitchens` (
  `soupKitchenId` int(16) UNSIGNED NOT NULL,
  `description` varchar(255) NOT NULL,
  `hours` varchar(255) NOT NULL,
  `conditions` varchar(255) NOT NULL,
  `seats` int(16) UNSIGNED NOT NULL,
  `siteIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `soupKitchens`
--

INSERT INTO `soupKitchens` (`soupKitchenId`, `description`, `hours`, `conditions`, `seats`, `siteIdFk`) VALUES
(2, 'soup2', 'Wednesdays 2-6pm', 'Picture ID/driver license', 10, 2),
(3, 'soup3', '8:00am-8:00pm', 'Photo ID', 50, 3),
(13, 'soup kitchen #1', '7/24', 'ssn', 100, 1);

-- --------------------------------------------------------

--
-- Table structure for table `storageTypes`
--

CREATE TABLE `storageTypes` (
  `storageId` int(16) UNSIGNED NOT NULL,
  `storageType` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `storageTypes`
--

INSERT INTO `storageTypes` (`storageId`, `storageType`) VALUES
(1, 'Dry Good'),
(2, 'Refrigerated'),
(3, 'Frozen');

-- --------------------------------------------------------

--
-- Table structure for table `subCategories`
--

CREATE TABLE `subCategories` (
  `subCatId` int(16) UNSIGNED NOT NULL,
  `subcategory` varchar(30) NOT NULL,
  `catIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subCategories`
--

INSERT INTO `subCategories` (`subCatId`, `subcategory`, `catIdFk`) VALUES
(1, 'Vegetables', 1),
(2, 'nuts/grains/beans', 1),
(3, 'Meat/seafood', 1),
(4, 'Dairy/eggs', 1),
(5, 'Sauce/Condiment/Seasoning', 1),
(6, 'Juice/Drink', 1),
(7, 'Personal hygiene', 2),
(8, 'Clothing', 2),
(9, 'Shelter', 2),
(10, 'other', 2);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `userId` int(16) UNSIGNED NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(30) NOT NULL,
  `email` varchar(255) NOT NULL,
  `fullName` varchar(255) NOT NULL,
  `siteIdFk` int(16) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`userId`, `username`, `password`, `email`, `fullName`, `siteIdFk`) VALUES
(1, 'emp1', 'gatech123', 'emp1@asacs.com', 'Site1 Emplyee1', 1),
(2, 'emp2', 'gatech123', 'emp2@asacs.com', 'Site2 Emplyee2', 2),
(3, 'emp3', 'gatech123', 'emp3@asacs.com', 'Site3 Emplyee3', 3),
(4, 'vol1', 'gatech123', 'vol1@asacs.com', 'Site1 Volunteer1', 1),
(5, 'vol2', 'gatech123', 'vol2@asacs.com', 'Site2 Volunteer2', 2),
(6, 'vol3', 'gatech123', 'vol3@asacs.com', 'Site3 Volunteer3', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bunks`
--
ALTER TABLE `bunks`
  ADD PRIMARY KEY (`shelterIdFk`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`catId`);

--
-- Indexes for table `clientLogs`
--
ALTER TABLE `clientLogs`
  ADD PRIMARY KEY (`clientLogId`),
  ADD KEY `clientIdFk` (`clientIdFk`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- Indexes for table `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`clientId`);

--
-- Indexes for table `foodBanks`
--
ALTER TABLE `foodBanks`
  ADD PRIMARY KEY (`foodBankId`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- Indexes for table `foodPantries`
--
ALTER TABLE `foodPantries`
  ADD PRIMARY KEY (`foodPantryId`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`itemId`),
  ADD KEY `subCatIdFk` (`subCatIdFk`),
  ADD KEY `storageIdFk` (`storageIdFk`),
  ADD KEY `foodBankIdFk` (`foodBankIdFk`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`requestId`),
  ADD KEY `makingUserFk` (`makingUserFk`),
  ADD KEY `approvingUserFk` (`approvingUserFk`),
  ADD KEY `itemIdFk` (`itemIdFk`),
  ADD KEY `foodBankIdFk` (`foodBankIdFk`);

--
-- Indexes for table `shelters`
--
ALTER TABLE `shelters`
  ADD PRIMARY KEY (`shelterId`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- Indexes for table `sites`
--
ALTER TABLE `sites`
  ADD PRIMARY KEY (`siteId`),
  ADD UNIQUE KEY `siteName` (`siteName`);

--
-- Indexes for table `soupKitchens`
--
ALTER TABLE `soupKitchens`
  ADD PRIMARY KEY (`soupKitchenId`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- Indexes for table `storageTypes`
--
ALTER TABLE `storageTypes`
  ADD PRIMARY KEY (`storageId`);

--
-- Indexes for table `subCategories`
--
ALTER TABLE `subCategories`
  ADD PRIMARY KEY (`subCatId`),
  ADD KEY `catIdFk` (`catIdFk`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`userId`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `siteIdFk` (`siteIdFk`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `catId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `clientLogs`
--
ALTER TABLE `clientLogs`
  MODIFY `clientLogId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;
--
-- AUTO_INCREMENT for table `clients`
--
ALTER TABLE `clients`
  MODIFY `clientId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `foodBanks`
--
ALTER TABLE `foodBanks`
  MODIFY `foodBankId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- AUTO_INCREMENT for table `foodPantries`
--
ALTER TABLE `foodPantries`
  MODIFY `foodPantryId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `itemId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;
--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `requestId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=107;
--
-- AUTO_INCREMENT for table `shelters`
--
ALTER TABLE `shelters`
  MODIFY `shelterId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `sites`
--
ALTER TABLE `sites`
  MODIFY `siteId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=91;
--
-- AUTO_INCREMENT for table `soupKitchens`
--
ALTER TABLE `soupKitchens`
  MODIFY `soupKitchenId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
--
-- AUTO_INCREMENT for table `storageTypes`
--
ALTER TABLE `storageTypes`
  MODIFY `storageId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `subCategories`
--
ALTER TABLE `subCategories`
  MODIFY `subCatId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `userId` int(16) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93121;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `bunks`
--
ALTER TABLE `bunks`
  ADD CONSTRAINT `bunks_ibfk_1` FOREIGN KEY (`shelterIdFk`) REFERENCES `shelters` (`shelterId`);

--
-- Constraints for table `clientLogs`
--
ALTER TABLE `clientLogs`
  ADD CONSTRAINT `clientLogs_ibfk_1` FOREIGN KEY (`clientIdFk`) REFERENCES `clients` (`clientId`),
  ADD CONSTRAINT `clientLogs_ibfk_2` FOREIGN KEY (`siteIdFk`) REFERENCES `sites` (`siteId`);

--
-- Constraints for table `foodBanks`
--
ALTER TABLE `foodBanks`
  ADD CONSTRAINT `foodBanks_ibfk_1` FOREIGN KEY (`siteIdFk`) REFERENCES `sites` (`siteId`);

--
-- Constraints for table `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`subCatIdFk`) REFERENCES `subCategories` (`subCatId`),
  ADD CONSTRAINT `items_ibfk_2` FOREIGN KEY (`storageIdFk`) REFERENCES `storageTypes` (`storageId`),
  ADD CONSTRAINT `items_ibfk_3` FOREIGN KEY (`foodBankIdFk`) REFERENCES `foodBanks` (`foodBankId`);

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`makingUserFk`) REFERENCES `users` (`userId`),
  ADD CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`approvingUserFk`) REFERENCES `users` (`userId`),
  ADD CONSTRAINT `requests_ibfk_3` FOREIGN KEY (`itemIdFk`) REFERENCES `items` (`itemId`),
  ADD CONSTRAINT `requests_ibfk_4` FOREIGN KEY (`foodBankIdFk`) REFERENCES `foodBanks` (`foodBankId`);

--
-- Constraints for table `subCategories`
--
ALTER TABLE `subCategories`
  ADD CONSTRAINT `subCategories_ibfk_1` FOREIGN KEY (`catIdFk`) REFERENCES `categories` (`catId`);

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`siteIdFk`) REFERENCES `sites` (`siteId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
