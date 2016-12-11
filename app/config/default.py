# -*- coding: utf-8 -*-
from __future__ import unicode_literals

PORT = 6500
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 14

SESSION_COOKIE_NAME = "_vua_s"

BASE_URL = "https://api.voxity.fr/api/v1"
AUTHORIZATION_BASE_URL = BASE_URL + '/dialog/authorize'
TOKEN_URL = BASE_URL + '/oauth/token'

CLIENT_ID = None
CLIENT_SECRET = None
REDIRECT_URI = "http://127.0.0.1:6500/account/signin-callback"
SECRET_KEY = "azerty"
DEBUG = True

OAUTHLIB_INSECURE_TRANSPORT = '1'
TRACKER_FILE = None

DASHBOARD_VIEW = "DEVICES.index"
LOGOUT_URI = "/account/signin-check"
INDEX_PAGE_URI = LOGOUT_URI
CHANGELOG_URI = '/changelog'
ABOUT_URI = '/about.html'