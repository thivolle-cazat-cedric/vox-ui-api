# Projet d'interface simplifé

Basé sur [l'API Voxity](https://client.voxity.fr/doc). Cette interface vous permet de :
 - [X] lister vos contacts
 - [X] Lister vos numéro interne & connaitre leurs état d'enregistrement
 - [-] Génerer des appels
 - [ ] Voir votre journal d'appel

-----

# Requierment
 - Python & pip
 - Virtualenv
 - Acces au site client.voxity.fr pour générer ces CLIENT_ID/CLIENT_SECRET

# Instalation

## Création des acces à l'API


 1. Aller sur le site [votre compte voxity](https://client.voxity.fr/voxity-api/configuration)
 2. cliquer sur **+**
    - non : test ui api
    - Url de redirection : http://127.0.0.1:6500/callback
 3. Récuperer votre client_id et votre client_secret

## Installation du projet

```bash
$ git clone ssh://git@git.voxity.fr:2288/cedric/voxity-ui-api.git
$ cd voxity-ui-api
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirement.txt
(venv) $ echo "# -*- coding: utf-8 -*-

CLIENT_ID = '<your_client_id>
CLIENT_SECRET = '<your_client_secret>'
SECRET_KEY = '<randum>'
" > app/config/env/prod.py
```

-----

# Lancement de l'Application

```
(venv) $ python main.py
```
Aller sur 127.0.0.1:6500