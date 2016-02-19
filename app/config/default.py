# -*- coding: utf-8 -*-
from __future__ import unicode_literals

BASE_URL = "https://api.voxity.fr/api/v1"
AUTHORIZATION_BASE_URL = 'https://api.voxity.fr/api/v1/dialog/authorize'
TOKEN_URL = 'https://api.voxity.fr/api/v1/oauth/token'
CLIENT_ID = None
CLIENT_SECRET = None
PORT = 6500
REDIRECT_URI = "http://127.0.0.1:6500/callback"

SECRET_KEY = "azerty"
DEBUG = True
OAUTHLIB_INSECURE_TRANSPORT = '1'

PERMANENT_SESSION_LIFETIME = 3600 * 24 * 7
