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
  PRIMARY KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `communique`
--

LOCK TABLES `communique` WRITE;
/*!40000 ALTER TABLE `communique` DISABLE KEYS */;
INSERT INTO `communique` VALUES ('2020-04-15',15,0,14,227,121,0,0,0),('2020-04-16',21,0,19,435,138,0,0,0);
/*!40000 ALTER TABLE `communique` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ligne_com_local`
--

DROP TABLE IF EXISTS `ligne_com_local`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ligne_com_local` (
  `date` date NOT NULL,
  `id_localite` int(11) NOT NULL,
  PRIMARY KEY (`date`,`id_localite`),
  KEY `fk_local` (`id_localite`),
  CONSTRAINT `fk_date` FOREIGN KEY (`date`) REFERENCES `communique` (`date`),
  CONSTRAINT `fk_local` FOREIGN KEY (`id_localite`) REFERENCES `localites` (`id_localite`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ligne_com_local`
--

LOCK TABLES `ligne_com_local` WRITE;
/*!40000 ALTER TABLE `ligne_com_local` DISABLE KEYS */;
INSERT INTO `ligne_com_local` VALUES ('2020-04-16',27),('2020-04-16',28),('2020-04-16',29),('2020-04-16',30),('2020-04-16',31),('2020-04-16',32),('2020-04-16',33),('2020-04-16',34),('2020-04-16',35),('2020-04-16',36),('2020-04-16',37),('2020-04-16',38),('2020-04-16',39);
/*!40000 ALTER TABLE `ligne_com_local` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `localites`
--

DROP TABLE IF EXISTS `localites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localites` (
  `id_localite` int(11) NOT NULL AUTO_INCREMENT,
  `nom` varchar(30) DEFAULT NULL,
  `nbCas` int(11) DEFAULT NULL,
  PRIMARY KEY (`id_localite`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localites`
--

LOCK TABLES `localites` WRITE;
/*!40000 ALTER TABLE `localites` DISABLE KEYS */;
INSERT INTO `localites` VALUES (1,'Dakar',0),(2,'ThiÃ¨s',0),(3,'Diourbel',0),(4,'Fatick',0),(5,'Kaolack',0),(6,'Kaffrine',0),(7,'Touba',4),(8,'Kolda',0),(9,'Tamba',0),(10,'Ziguinchor',0),(11,'Saint-Louis',0),(12,'Matam',0),(13,'SÃ©dhiou',0),(14,'Dakar',0),(15,'ThiÃ¨s',0),(16,'Diourbel',0),(17,'Fatick',0),(18,'Kaolack',0),(19,'Kaffrine',0),(20,'Touba',0),(21,'Kolda',0),(22,'Tamba',0),(23,'Ziguinchor',0),(24,'Saint-Louis',0),(25,'Matam',0),(26,'SÃ©dhiou',0),(27,'Dakar',0),(28,'ThiÃ¨s',0),(29,'Diourbel',0),(30,'Fatick',0),(31,'Kaolack',0),(32,'Kaffrine',0),(33,'Touba',0),(34,'Kolda',0),(35,'Tamba',0),(36,'Ziguinchor',0),(37,'Saint-Louis',0),(38,'Matam',0),(39,'SÃ©dhiou',0);
/*!40000 ALTER TABLE `localites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `test`
--

DROP TABLE IF EXISTS `test`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `test` (
  `id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `test`
--

LOCK TABLES `test` WRITE;
/*!40000 ALTER TABLE `test` DISABLE KEYS */;
/*!40000 ALTER TABLE `test` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-05-07  1:42:58
