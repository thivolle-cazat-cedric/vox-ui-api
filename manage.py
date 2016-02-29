#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask.ext.script import Manager

from app import create_app
from app.utils import random_string
from os import environ


app = create_app()
environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config['OAUTHLIB_INSECURE_TRANSPORT']

manager = Manager(app)

@manager.command
def generate_key():
    print(random_string(
    	min_size=32,
    	max_size=128,
    	punctuation=True,
    	exposant=6
    ))

if __name__ == "__main__":
    manager.run()