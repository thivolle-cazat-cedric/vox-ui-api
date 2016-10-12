# vox ui api website
-----

# Installation

## Requierment
 - Python & pip
 - Virtualenv
 - Acces au site client.voxity.fr pour générer ces CLIENT_ID/CLIENT_SECRET

```bash
git clone ssh://git@baltig.thivolle-cazat.fr:2288/root/vox-ui-api-website.git
cd voxity-ui-api-website
virtualenv .env
source .env/bin/activate
pip install -r requirement.txt
mkdir app/config/env
touch app/config/env/__init__.py app/config/env/prod.py
key=`./manage.py generate_key`
echo "SECRET_KEY = '''$key'''" > app/config/env/prod.py
```

-----

# Lancement de l'Application

```
(venv) $ ./manage.py runserver -p 6501
```

L'appliaction est lancé sur l'uri [127.0.0.1:6501](http://127.0.0.1:6501)