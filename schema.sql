CREATE DATABASE `TW_STOCK` /*!40100 DEFAULT CHARACTER SET utf8 */;

CREATE TABLE `DAILY_TRADE` (
  `ID` varchar(10) NOT NULL,
  `TYPE` varchar(1) NOT NULL COMMENT 'L: Listed companies; O: Over the Counter companies.',
  `TRADE_DATE` date NOT NULL,
  `OPEN` decimal(10,2) NOT NULL,
  `HIGH` decimal(10,2) NOT NULL,
  `LOW` decimal(10,2) NOT NULL,
  `CLOSE` decimal(10,2) NOT NULL,
  `VOL` bigint(20) NOT NULL,
  `FII_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Foreign Investment Institution capital',
  `DI_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Domestic Institution capital',
  `DEALER_CAPITAL` bigint(20) DEFAULT NULL COMMENT 'Dealer capital',
  `PER` decimal(7,2) DEFAULT NULL COMMENT 'Price Earning Ratio',
  PRIMARY KEY (`ID`,`TYPE`,`TRADE_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY KEY (TRADE_DATE)
PARTITIONS 12 */;

CREATE TABLE `DAILY_INDEX` (
  `ID` varchar(10) NOT NULL,
  `TYPE` varchar(1) NOT NULL COMMENT 'L: Listed companies; O: Over the Counter companies.',
  `TRADE_DATE` date NOT NULL,
  `MA_CLOSE_5` decimal(10,2) DEFAULT NULL COMMENT '5 day moving average of close price',
  `MA_CLOSE_20` decimal(10,2) DEFAULT NULL COMMENT '20 day moving average of close price',
  `MA_CLOSE_60` decimal(10,2) DEFAULT NULL COMMENT '60 day moving average of close price',
  PRIMARY KEY (`ID`,`TYPE`,`TRADE_DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY KEY (TRADE_DATE)
PARTITIONS 12 */;
