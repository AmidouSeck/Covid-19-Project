******************************* COMMENT UTILISER LE MODULE 1 ******************************************

Apres avoir éxécuté le programme, le module 1 ou data acquisition est l'onglet par defaut qui s'affiche
presentant un message de bienvenu et un buton permettant en un clic de télécharger tous les communiqués
et de les extraire sous forme de fichier JSON. Communiqués qu'on peut retrouver en PDF dans le dossier
PDF du programme et en JSON dans le Dossier JSON.


NB: le téléchargement et l'extraction peut durer selon la responsivité du site du ministere et selon
votre connexion internet.


***********************************COMMENT UTILISER LE MODULE 2 ****************************************

Après le téléchargement et l'extraction, il est question ici d'importer les données vers la base de données
dans ce module (data loader). C'est pour cela qu'un buton "select" est conçu pour permettre a l'utilisateur 
de selectionner les données de son choix.
Une fois selectionnés le mois et l'année, il a la possibilité de séléctionner aussi les jours du mois qu'il
veut importer. En cliquant sur le buton "import", il est améné à s'authentifier et décider si les données
seront en mode transactionnel ou pas en cochant l'option mode transactionnel.
Pour rappel, le mode transactionnel permet de valider (commit) l'importation ou non (rollback).
Une fois terminé, un pop up s'affichera lui notifiant si oui ou non les données séléctionnées sont importés
vers la base de données. Ainsi il pourra passer au module suivant.


******************************* COMMENT UTILISER LE MODULE 3 ******************************************

Apres avoir importé les données vers la base de données, le module 3 a pour principal objectif d'afficher
celles-ci sur la carte geographique du Sénegal.
En cliquant sur le buton 'explore', vous serez améné bien  sur à vous authentifier encore. Une fois réussi,
la carte se generera automatiquement et representant les données (nombre de cas) pour chaque région du Sénegal.
