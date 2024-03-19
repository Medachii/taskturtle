# Taskturtle

Voici comment tout démarrer : 

Tout d'abord, se placer dans project07/taskturtle.

Notre contrat est situé à ./contracts/smartcontract.sol.
Il faut le copier dans Remix IDE, le compiler et le déployer. En le déployant, on obtient une nouvelle adresse de contrat, à remplacer dans ./backend/app.py à la ligne 21.
En parallèle, on utilise l'interface grpahique de Ganache pour créer une blockchain de test. Il faut connecter Remix IDE à la blockchain Ganache sélectionnant comme environnement "External Http Provider" et en précisant la bonne adresse spécifiée par Ganache.

Avec ça, Ganache et Remix sont connectés. Les modifications dans Remix sont répercutées vers Ganache.

Ensuite, il faut démarrer l'application.
D'abord, il faut lancer `npm run start-backend` pour lancer le côté serveur.
Ensuite, `npm run start` lance l'application.

La base de données est située à ./backend/database/projects.db.
Il n'y a rien dans la table transactions. Il faut que les transactions dans la base de données soient synchronisées avec celles de la blockchain.
Au cas-où, il est possible de supprimer ./backend/database/projects.db et de lancer la commande `sqlite3 projects.db`, et ensuite `.read projects.sql` pour avoir une base de données initiale.

Pour se connecter, il y a 3 comptes déjà présents dans la table : 
email : test1@test1.fr, mot de passe : test1, id : 1
email : test2@test2.fr, mot de passe : test2, id : 2
