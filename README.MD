# Projet d'interface simplifié

Basé sur [l'API Voxity](https://api.voxity.fr/doc). Cette interface vous permet de :

 - Lister et rechercher vos contacts
 - Lister les postes & connaitre leurs états
 - Générer des appels
 - Notification de bureau *lors d'appels entrants*

Retrouvez le site démonstration : [vox-ui-api](http://vox-ui-api.webstartapp.fr)

-----

# Requierment
 - Python & pip
 - Virtualenv
 - Acces au site client.voxity.fr pour générer ces CLIENT_ID/CLIENT_SECRET

# Installation

## Création des accès à l'API


 1. Aller sur le site [votre compte voxity](https://client.voxity.fr/voxity-api/configuration)
 2. Cliquer sur **+**
    - Non : test ui api
    - Url de redirection : http://127.0.0.1:6500/callback
 3. Récupérer votre client_id et votre client_secret

## Installation du projet

```bash
$ git clone --recursive ssh://git@baltig.thivolle-cazat.fr:2288/root/voxity-ui-api.git
$ cd voxity-ui-api
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirement.txt
(venv) $ key=`./manage.py generate_key`
(venv) $ echo "
CLIENT_ID = '<your_client_id>
CLIENT_SECRET = '<your_client_secret>'
SECRET_KEY = '$key'
" > app/config/env/prod.py
```

-----

# Lancement de l'Application

```
(venv) $ ./manage.py runserver -p 6500
```

L'appliaction est lancer sur l'uri [127.0.0.1:6500](http://127.0.0.1:6500)