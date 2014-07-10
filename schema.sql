CREATE DATABASE `TW_STOCK` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `DAILY_TRADE` (
  `ID` varchar(10) NOT NULL,
  `TRADE_DATE` date NOT NULL,
  `TYPE` varchar(1) NOT NULL COMMENT 'L: Listed companies; O: Over the Counter companies.',
  `OPEN` decimal(10,2) unsigned NOT NULL,
  `HIGH` decimal(10,2) unsigned NOT NULL,
  `LOW` decimal(10,2) unsigned NOT NULL,
  `CLOSE` decimal(10,2) unsigned NOT NULL,
  `VOL` bigint(20) unsigned NOT NULL,
  `FII_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Foreign Investment Institution capital',
  `DI_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Domestic Institution capital',
  `DEALER_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Dealer capital',
  PRIMARY KEY (`ID`,`TRADE_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
