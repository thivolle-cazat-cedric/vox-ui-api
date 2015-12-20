#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import create_app
from os import environ

# This information is obtained upon registration of a new GitHub OAuth


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    app = create_app()
    environ['OAUTHLIB_INSECURE_TRANSPORT'] = app.config['OAUTHLIB_INSECURE_TRANSPORT']
    app.run(debug=True, port=6500)
