-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 26, 2018 at 09:48 PM
-- Server version: 5.7.23-0ubuntu0.18.04.1
-- PHP Version: 7.2.10-0ubuntu0.18.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cryptocurrency`
--

-- --------------------------------------------------------

--
-- Table structure for table `finex_history`
--

CREATE TABLE `finex_history` (
  `timestamp` int(10) UNSIGNED NOT NULL,
  `open` float NOT NULL,
  `close` float NOT NULL,
  `high` float NOT NULL,
  `low` float NOT NULL,
  `volume` float NOT NULL,
  `utc_datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

-- --------------------------------------------------------

--
-- Table structure for table `gdax_history`
--

CREATE TABLE `gdax_history` (
  `timestamp` int(10) UNSIGNED NOT NULL,
  `low` float NOT NULL,
  `high` float NOT NULL,
  `open` float NOT NULL,
  `close` float NOT NULL,
  `volume` float NOT NULL,
  `utc_datetime` datetime NOT NULL,
  `mt_datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `finex_history`
--
ALTER TABLE `finex_history`
  ADD PRIMARY KEY (`timestamp`);

--
-- Indexes for table `gdax_history`
--
ALTER TABLE `gdax_history`
  ADD PRIMARY KEY (`timestamp`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
