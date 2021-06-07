******************************* COMMENT UTILISER LE MODULE 1 ******************************************

Apres avoir �x�cut� le programme, le module 1 ou data acquisition est l'onglet par defaut qui s'affiche
presentant un message de bienvenu et un buton permettant en un clic de t�l�charger tous les communiqu�s
et de les extraire sous forme de fichier JSON. Communiqu�s qu'on peut retrouver en PDF dans le dossier
PDF du programme et en JSON dans le Dossier JSON.


NB: le t�l�chargement et l'extraction peut durer selon la responsivit� du site du ministere et selon
votre connexion internet.


***********************************COMMENT UTILISER LE MODULE 2 ****************************************

Apr�s le t�l�chargement et l'extraction, il est question ici d'importer les donn�es vers la base de donn�es
dans ce module (data loader). C'est pour cela qu'un buton "select" est con�u pour permettre a l'utilisateur 
de selectionner les donn�es de son choix.
Une fois selectionn�s le mois et l'ann�e, il a la possibilit� de s�l�ctionner aussi les jours du mois qu'il
veut importer. En cliquant sur le buton "import", il est am�n� � s'authentifier et d�cider si les donn�es
seront en mode transactionnel ou pas en cochant l'option mode transactionnel.
Pour rappel, le mode transactionnel permet de valider (commit) l'importation ou non (rollback).
Une fois termin�, un pop up s'affichera lui notifiant si oui ou non les donn�es s�l�ctionn�es sont import�s
vers la base de donn�es. Ainsi il pourra passer au module suivant.


******************************* COMMENT UTILISER LE MODULE 3 ******************************************

Apres avoir import� les donn�es vers la base de donn�es, le module 3 a pour principal objectif d'afficher
celles-ci sur la carte geographique du S�negal.
En cliquant sur le buton 'explore', vous serez am�n� bien  sur � vous authentifier encore. Une fois r�ussi,
la carte se generera automatiquement et representant les donn�es (nombre de cas) pour chaque r�gion du S�negal.
