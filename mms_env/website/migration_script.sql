-- ----------------------------------------------------------------------------
-- MySQL Workbench Migration
-- Migrated Schemata: locationapp
-- Source Schemata: flasklocationapp
-- Created: Thu Jun 30 09:39:19 2022
-- Workbench Version: 8.0.29
-- ----------------------------------------------------------------------------

SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- Schema locationapp
-- ----------------------------------------------------------------------------
DROP SCHEMA IF EXISTS `locationapp` ;
CREATE SCHEMA IF NOT EXISTS `locationapp` ;

-- ----------------------------------------------------------------------------
-- Table locationapp.location
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `locationapp`.`location` (
  `idlocation` INT NOT NULL AUTO_INCREMENT,
  `gpsdata` VARCHAR(45) NOT NULL,
  `capturedatetime` DATETIME NOT NULL,
  `truckid` INT NOT NULL,
  PRIMARY KEY (`idlocation`),
  INDEX `truckloc_idx` (`truckid` ASC) VISIBLE,
  CONSTRAINT `truckloc`
    FOREIGN KEY (`truckid`)
    REFERENCES `locationapp`.`truck` (`idtruck`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Table locationapp.truck
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS `locationapp`.`truck` (
  `idtruck` INT NOT NULL AUTO_INCREMENT,
  `registration` VARCHAR(10) NOT NULL,
  PRIMARY KEY (`idtruck`, `registration`))
ENGINE = InnoDB
AUTO_INCREMENT = 22
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------------------------------------------------------
-- Routine locationapp.getAllGpsData
-- ----------------------------------------------------------------------------
DELIMITER $$

DELIMITER $$
USE `locationapp`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `getAllGpsData`(
IN truckid INT,
IN datetimeVar DATETIME
)
BEGIN
SELECT idlocation, gpsdataS, gpsdataE FROM location WHERE truckid = truckid AND capturedatetime = DATE(datetimeVar);
END$$

DELIMITER ;
SET FOREIGN_KEY_CHECKS = 1;
