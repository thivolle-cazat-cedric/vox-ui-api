# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from markdown2 import markdown

PUBLIC = Blueprint('PUBLIC',
    __name__,
    template_folder='templates',
    url_prefix='',
    static_folder='static'
)

DESC = "Projet libre d'application web présentant les possibilités "
DESC += "d'intégration de l'API Voxity. Click2call, notification "
DESC += "d'appels, envoie de SMS, gestion des contacts. Un tableau"
DESC += " de bord pour visualiser l'état de votre parc téléphonique"
DESC += " type BLF."
TAGS = [
    "Voxity",
    "API",
    "Application web",
    "SMS",
    "Notification d'appels",
    "etat des postes",
    "Samples",
    "Exemple",
    "vox-ui-api",
    "voxity-ui-api",
    "voxity user interface api",
]


@PUBLIC.route("/")
@PUBLIC.route("/index.html")
def index():
    return render_template(
        'public/index.html',
        meta_desc=DESC,
        meta_keywords_list=TAGS
    )


@PUBLIC.route('/changelog.html', methods=["GET"])
def changelog():
    local_tag = TAGS
    local_tag.append('Évolution')
    local_tag.append('Mise à jour')
    return render_template(
        'public/changelog.html',
        meta_keywords_list=TAGS,
        changelog=markdown(render_template('changelog.md')),
        page_title="changelog"
    )


@PUBLIC.route('/about.html', methods=["GET"])
def about(): 
    return render_template(
        'public/about.html',
        page_title="à propos"
    )


@PUBLIC.route('/features.html', methods=["GET"])
def features():
    return render_template(
        'public/features.html',
        page_title="fonctionalités",
        meta_keywords_list=TAGS
    )


@PUBLIC.route('/screenshot.html', methods=["GET"])
def screen():
    return render_template(
        'public/screen.html',
        page_title="Captures d'écran",
        meta_keywords_list=TAGS
    )


@PUBLIC.route('/sitemap.xml', methods=["GET"])
def sitemap():
    return render_template('public/sitemap.xml'), 200, {'Content-Type': 'text/xml; charset=utf-8'}
