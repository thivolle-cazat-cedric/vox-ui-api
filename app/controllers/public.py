# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from markdown2 import markdown

PUBLIC = Blueprint('PUBLIC', __name__)

DESC = "Projet public d'application web présentant les possibilités d'intégration de"
DESC += " l'A.P.I. Voxity. Click2call, notification d'appels, consultation de l'état'"
DESC += " des postes, envoie de SMS."
TAGS = [
    "Voxity",
    "API",
    "Application web",
    "SMS",
    "Notification d'appels",
    "etat des postes",
    "Samples",
    "Exemple",
    "vox-ui-api"
]


@PUBLIC.route("")
@PUBLIC.route("index.html")
def index():
    return render_template(
        'public/index.html',
        meta_desc=DESC,
        meta_keywords_list=TAGS
    )


@PUBLIC.route('changelog.html', methods=["GET"])
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


@PUBLIC.route('about.html', methods=["GET"])
def about(): 
    return render_template(
        'public/about.html',
        page_title="à propos"
    )


@PUBLIC.route('features.html', methods=["GET"])
def features():
    return render_template('public/features.html', page_title="fonctionalités")
