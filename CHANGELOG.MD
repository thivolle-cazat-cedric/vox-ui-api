# Changelog

---

##### Bug*(s)* connu*(s)*

 - [ ] Journal d'appel *(non-fonctionnel)*
 - [-] Authentification *l'application peut parfois vous retourner des erreurs 401 sans raison valable*


#Version 1 

---

### 1.1 βeta [:danger: en cours]

 - [X] Ajout d'un contact 
 - [X] Édition d'un contact
 - [ ] Déconnexion *(la déconnexion n'est pas fonctionnelle, il faut ce déconnecter via l'API directement)*

### 1.0 βeta

##### 1.0.6
###### Nouveautés
 - Lorsqu'un contact possède un numéro de mobile, vous avez un lien direct pour lui envoyer un SMS.
 - Ajout d'une correspondance nom/numéro dans le journal d'appel. *(non-fonctionnel)*

###### Améliorations & Corrections
 - Amélioration de l'envoi de SMS, vous n'êtes plus obligé de renseigner un nom d'émetteur.
 - Amélioration des droits dans l'application. Un nom administrateur ne peut pas ajouter, modifier, supprimer de contact.
 - Amélioration de la vue d'un poste, on affiche le numéro appelé, le nom de l'appelant. *(dans le cas ou la case **remplacer le numéro par la description** dans octopus)*
 - Correction d'un bug lors de l'affichage de tout le journal d'appel.

##### 1.0.5
 - Intégration des SMS, listing et envoi unique ou multiple
 - Mise à jour du fichier de déploiment sur apache2 *(redémarrage automatique lors de la modification d'un fichier)*
 - Amélioration de l'affichage des boutons **édition** et **suppression** des contacts

##### 1.0.4
 - Correction d'un bug lors d'un raccroché *lorsque que vous êtes actif sur la page*
 - Correction d'un bug lors d'un appel décroché
 - Gestion des contacts *(ajout, modification, suppression)*
 
##### 1.0.3
 - Résolution de problème de notification de bureau sur certains navigateurs
 - Ajout d'une notification si votre poste se déconnecte de la plate-forme Voxity

##### 1.0.2
 - Résolution du bug sur le tableau de bord quand un poste est en attente
 - Traduction des états de post en français  
 - Ajout d'un raccourci *h* pour retourner au tableau de bord à tous moment
 - Désactivation des notifications de bureau dans le cas ou la page est active
 - Amélioration du tableau de bord *(3 colonnes pour les écrans large, 2 pour les écrans moyens et 1 pour les petits écrans)*

##### 1.0.1
 - [X] Ajout d'un lien de déconnexion dans la page d'accueil

### αlpha

---
##### Fonctionnalités :

 - [X] Liste des téléphones avec états du poste
 - [X] Notifications lors d'un appel entrant *(notification de bureau)*
 - [X] Liste des contacts présents dans l'annuaire
 - [X] Click to Call
 - [X] Génération d'appel
 - [X] Remplacement des numéros connus par un nom *(si présent dans l'annuaire)*
 - [X] Recherche de contact