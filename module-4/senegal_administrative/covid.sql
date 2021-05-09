-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: covid
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `communique`
--

DROP TABLE IF EXISTS `communique`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `communique` (
  `date` date NOT NULL,
  `casPositifs` int(11) DEFAULT NULL,
  `casImportes` int(11) DEFAULT NULL,
  `casContacts` int(11) DEFAULT NULL,
  `testRealises` int(11) DEFAULT NULL,
  `sousTraitement` int(11) DEFAULT NULL,
  `casCommunautaires` int(11) DEFAULT NULL,
  `casGueris` int(11) DEFAULT NULL,
  `deces` int(11) DEFAULT NULL,
  `id_localite` int(11) DEFAULT NULL,
  PRIMARY KEY (`date`),
  KEY `fk_localite` (`id_localite`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communique`
--

LOCK TABLES `communique` WRITE;
/*!40000 ALTER TABLE `communique` DISABLE KEYS */;
INSERT INTO `communique` VALUES ('2020-04-16',21,0,19,435,138,0,0,0,1),('2020-04-20',10,0,5,281,136,0,0,0,2),('2020-04-22',30,0,26,482,182,0,0,0,3);
/*!40000 ALTER TABLE `communique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `localite`
--

DROP TABLE IF EXISTS `localite`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localite` (
  `id_localite` int(11) NOT NULL AUTO_INCREMENT,
  `Dakar` int(11) DEFAULT '0',
  `Thies` int(11) DEFAULT '0',
  `Diourbel` int(11) DEFAULT '0',
  `Fatick` int(11) DEFAULT '0',
  `Kaolack` int(11) DEFAULT '0',
  `Kaffrine` int(11) DEFAULT '0',
  `Touba` int(11) DEFAULT '0',
  `Kolda` int(11) DEFAULT '0',
  `Tamba` int(11) DEFAULT '0',
  `Ziguinchor` int(11) DEFAULT '0',
  `SaintLouis` int(11) DEFAULT '0',
  `Matam` int(11) DEFAULT '0',
  `Sedhiou` int(11) DEFAULT '0',
  `Kedougou` int(11) DEFAULT '0',
  `Louga` int(11) DEFAULT '0',
  `Tambacounda` int(11) DEFAULT '0',
  PRIMARY KEY (`id_localite`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localite`
--

LOCK TABLES `localite` WRITE;
/*!40000 ALTER TABLE `localite` DISABLE KEYS */;
INSERT INTO `localite` VALUES (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),(2,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0),(3,0,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0);
/*!40000 ALTER TABLE `localite` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-06 17:49:11
