# How to deploy this service on apach2

# Apache2

Pour déployer une instance de vox-ui-api sur votre serveur via apache, vous avez besoin du module apache mod_uwsgi

pour activer / installer le module, voici un exemple sur un ubutu : 

```
# apt-get update && apt install libapache2-mod-wsgi
# a2enmod wsgi
# service apache restart
```

Ensuite vous aurez besoin de creer 2 fichiers : 
 
 1. le fichier python contenant la variable application pour uwsgi (([voir fichier exemple](app.wsgi)))
 2. un vhost ([voir fichier exemple](vhost.conf))

Pour ces 2 fichiers vous aurez besoin du chemin absolut de votre virualenv, et du chemin pour arriver à la racine du projet