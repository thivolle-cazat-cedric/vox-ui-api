#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os
from os import environ
path_app = [path_to_root_project]
sys.path.insert(0, path_app)
os.chdir(path_app)

activate_this = [path_to_virualenv]/bin/activate_this #[path_to_root_project]/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
from app import create_app
application = create_app()
environ['OAUTHLIB_INSECURE_TRANSPORT'] = application.config['OAUTHLIB_INSECURE_TRANSPORT']