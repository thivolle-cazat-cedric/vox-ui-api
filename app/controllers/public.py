# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from markdown2 import markdown

PUBLIC = Blueprint('PUBLIC', __name__)


@PUBLIC.route("")
@PUBLIC.route("index.html")
def index():
    # if controllers.valide_session() and voxity.connectors() is not None:
    #     return redirect(url_for('DEVICES.devices_view'))

    # try:
    #     voxity.logout()
    # except Exception:
    #     controllers.clear_session()
    return render_template('public/index.html')


@PUBLIC.route('changelog.html', methods=["GET"])
def changelog():
    return render_template(
        'public/changelog.html',
        changelog=markdown(render_template('changelog.md'))
    )


@PUBLIC.route('about.html', methods=["GET"])
def about():
    return render_template(
        'public/about.html',
        changelog=markdown(render_template('changelog.md'))
    )
