# Covid-19 progression modeler

[![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)  [![forthebadge](http://forthebadge.com/images/badges/powered-by-electricity.svg)](http://forthebadge.com)

Covid-19 Progression Modeler est un projet visant à regrouper et analyser les données issues de la pandémie pour la compréhension de sa diffusion dans le territoire sénégalais

## Pour commencer

## Le Modéle Physique de Données
![alt text](https://github.com/AmidouSeck/Covid-19-Project/blob/dec813d478c0fb1beacdbf2080aa48b389e7508a/mpd.PNG?raw=true)

## Le Diagramme UML
![alt text](https://github.com/AmidouSeck/Covid-19-Project/blob/dec813d478c0fb1beacdbf2080aa48b389e7508a/diagramme_uml.PNG?raw=true)

### Contenu du projet


- Data Acquisition
  Module de téléchargement des fichiers pdf depuis le site officile du ministère de la santé afin d'extraire les données qui serviront d'analyse et de traitement.
- Data Loader
  Module d'insertion des données extraites depuis le module 1 dans la base MySQL avec mode AUTOCOMMIT ou TRANSACTION.
- Data Analyzer
Module d'analyse et d'interprétation des données insérées pour suivre l'évolution de la pandémie à travers des graphes
- Data Explorer
  Module pour suivre l'évolution journalière du nombre de cas des régions.

### Installation

Pour l'installations de l'ensemble des packages utilisés dans ce projet saisir la commande ci-dessous:
pip install -r requirements.txt

## Démarrage

En attente je mettrais ici ce qu'il faut

## Fabriqué avec

* [Python](https://www.python.org/) - Script
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Bibliotèque python pour interface graphique
* [MySql](https://www.mysql.com/fr/) - pur la base de données
* [VsCode](https://code.visualstudio.com/) - Éditeur de code


## Auteurs

* **Mohamed Amidou Seck** _alias_ [@AmidouSeck](https://github.com/AmidouSeck)
* **Demba Diack** _alias_ [@DembaDiack](https://github.com/DembaDiack)
* **Elhadj Ousmane** _alias_ [@ousmane12](https://github.com/ousmane12)
* **Ousmane Sow** _alias_ [@sow37](https://github.com/sow37)
* **Barka Amine Ahmath** _alias_ [@barkaamine72](https://github.com/barkaamine72)
* **Oumou Thiam** _alias_ [@oumouthiam](https://github.com/oumouthiam)

## License

Ce projet est sous licence ``ESP`` - voir le fichier [LICENSE.md](LICENSE.md) pour plus d'informations

