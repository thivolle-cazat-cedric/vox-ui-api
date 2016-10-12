# Voxity User Interface - API 

## Présentation de Vox-ui-api
###### Projet d'interface simplifiée

Basé sur [l'API Voxity](https://api.voxity.fr/doc). Cette interface vous permet de :

 - Gérer vos contacts
 - Lister les postes et connaitre leurs états
 - Générer des appels
 - Avoir des notifications de bureau *lors d'appels entrants, ou de déconnexion de son poste*
 - Connaitre avec qui est en ligne un poste

Retrouvez le site démonstration : [vox-ui-api.webstartapp.fr](http://vox-ui-api.webstartapp.fr)

L'application n'est pas proposée et ni supportée par Voxity. En cas de disfonctionnement, créez un ticket via l'outil Github 

-----

# Installation

## Requierment
 - Python & pip
 - Virtualenv
 - Acces au site client.voxity.fr pour générer ces CLIENT_ID/CLIENT_SECRET

## Création des accès à l'API


 1. Aller sur le site [votre compte voxity](https://client.voxity.fr/voxity-api/configuration)
 2. Cliquer sur **+**
    - Non : test ui api
    - Url de redirection : http://127.0.0.1:6500/account/signin-callback
 3. Récupérer votre client_id et votre client_secret

## Récupération et configuration de l'application

```bash
git clone --recursive https://github.com/thivolle-cazat-cedric/vox-ui-api.git
cd voxity-ui-api
virtualenv venv
source venv/bin/activate
pip install -r requirement.txt
touch app/config/env/prod.py
key=`./manage.py generate_key`
client_id=<your_client_id>
client_secret=<your_client_secret>
echo "CLIENT_ID = '''$client_id'''
CLIENT_SECRET = '''$client_secret'''
SECRET_KEY = '''$key'''
" > app/config/env/prod.py
```

-----

# Lancement de l'Application

```
(venv) $ ./manage.py runserver -p 6500
```

L'appliaction est lancé sur l'uri [127.0.0.1:6500](http://127.0.0.1:6500)