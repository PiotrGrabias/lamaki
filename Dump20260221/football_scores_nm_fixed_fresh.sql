-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: football_scores
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `nm_fixed_fresh`
--

DROP TABLE IF EXISTS `nm_fixed_fresh`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nm_fixed_fresh` (
  `id` int NOT NULL AUTO_INCREMENT,
  `match_date` date DEFAULT NULL,
  `league_name` varchar(255) DEFAULT NULL,
  `home_team` varchar(255) DEFAULT NULL,
  `away_team` varchar(255) DEFAULT NULL,
  `score` varchar(10) DEFAULT NULL,
  `match_result` varchar(255) DEFAULT NULL,
  `match_report_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6494 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nm_fixed_fresh`
--

LOCK TABLES `nm_fixed_fresh` WRITE;
/*!40000 ALTER TABLE `nm_fixed_fresh` DISABLE KEYS */;
INSERT INTO `nm_fixed_fresh` VALUES (6481,'2026-01-09','LEAGUE NIEMCY 2025','Eintracht Frankfurt','Borussia Dortmund','3-3','Eintracht Frankfurt 3-3 : Borussia Dortmund','https://www.whoscored.com/matches/1910678/live/germany-bundesliga-2025-2026-eintracht-frankfurt-borussia-dortmund'),(6482,'2026-01-10','LEAGUE NIEMCY 2025','Freiburg','Hamburger SV1','2-1','Freiburg 2-1 : Hamburger SV1','https://www.whoscored.com/matches/1910680/live/germany-bundesliga-2025-2026-freiburg-hamburger-sv'),(6483,'2026-01-13','LEAGUE NIEMCY 2025','VfB Stuttgart','Eintracht Frankfurt','3-2','VfB Stuttgart 3-2 : Eintracht Frankfurt','https://www.whoscored.com/matches/1910803/live/germany-bundesliga-2025-2026-vfb-stuttgart-eintracht-frankfurt'),(6484,'2026-01-13','LEAGUE NIEMCY 2025','Mainz 05','FC Heidenheim','2-1','Mainz 05 2-1 : FC Heidenheim','https://www.whoscored.com/matches/1910801/live/germany-bundesliga-2025-2026-mainz-05-fc-heidenheim'),(6485,'2026-01-14','LEAGUE NIEMCY 2025','Wolfsburg','St. Pauli','2-1','Wolfsburg 2-1 : St. Pauli','https://www.whoscored.com/matches/1910804/live/germany-bundesliga-2025-2026-wolfsburg-st-pauli'),(6486,'2026-01-14','LEAGUE NIEMCY 2025','FC Koln','Bayern Munich','1-3','FC Koln 1-3 : Bayern Munich','https://www.whoscored.com/matches/1910798/live/germany-bundesliga-2025-2026-fc-koln-bayern-munich'),(6487,'2026-01-16','LEAGUE NIEMCY 2025','Werder Bremen','Eintracht Frankfurt','3-3','Werder Bremen 3-3 : Eintracht Frankfurt','https://www.whoscored.com/matches/1910812/live/germany-bundesliga-2025-2026-werder-bremen-eintracht-frankfurt'),(6488,'2026-01-17','LEAGUE NIEMCY 2025','Borussia Dortmund','St. Pauli','3-2','Borussia Dortmund 3-2 : St. Pauli','https://www.whoscored.com/matches/1910806/live/germany-bundesliga-2025-2026-borussia-dortmund-st-pauli'),(6489,'2026-01-17','LEAGUE NIEMCY 2025','FC Koln','Mainz 05','2-1','FC Koln 2-1 : Mainz 05','https://www.whoscored.com/matches/1910807/live/germany-bundesliga-2025-2026-fc-koln-mainz-05'),(6490,'2026-01-24','LEAGUE NIEMCY 2025','Mainz 05','Wolfsburg','3-1','Mainz 05 3-1 : Wolfsburg','https://www.whoscored.com/matches/1910820/live/germany-bundesliga-2025-2026-mainz-05-wolfsburg'),(6491,'2026-01-24','LEAGUE NIEMCY 2025','Eintracht Frankfurt','Hoffenheim','1-3','Eintracht Frankfurt 1-3 : Hoffenheim','https://www.whoscored.com/matches/1910817/live/germany-bundesliga-2025-2026-eintracht-frankfurt-hoffenheim'),(6492,'2026-01-24','LEAGUE NIEMCY 2025','Bayern Munich','Augsburg','1-2','Bayern Munich 1-2 : Augsburg','https://www.whoscored.com/matches/1910815/live/germany-bundesliga-2025-2026-bayern-munich-augsburg'),(6493,'2026-01-25','LEAGUE NIEMCY 2025','Freiburg','FC Koln','2-1','Freiburg 2-1 : FC Koln','https://www.whoscored.com/matches/1910818/live/germany-bundesliga-2025-2026-freiburg-fc-koln');
/*!40000 ALTER TABLE `nm_fixed_fresh` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-21 10:09:26
