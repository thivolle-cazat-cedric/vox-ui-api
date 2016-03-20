# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from markdown2 import markdown

PUBLIC = Blueprint('PUBLIC', __name__)


@PUBLIC.route("")
@PUBLIC.route("index.html")
def index():
    return render_template('public/index.html')


@PUBLIC.route('changelog.html', methods=["GET"])
def changelog():
    return render_template(
        'public/changelog.html',
        changelog=markdown(render_template('changelog.md')),
        page_title="changelog"
    )


@PUBLIC.route('about.html', methods=["GET"])
def about():
    return render_template('public/about.html', page_title="à propos")


@PUBLIC.route('features.html', methods=["GET"])
def features():
    return render_template('public/features.html', page_title="fonctionalités")
