# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from oauthlib.oauth2 import TokenExpiredError
from flask import Blueprint, render_template, session, abort
from flask.json import jsonify
from app.voxity import self_user, logout, refresh_token
from app.controllers import is_auth



ACCOUNT = Blueprint('ACCOUNT', __name__)

LIST_AVAILABLE = [5, 10, 25, 50, 100]

def refresh_user_session():
    try:
        session['user'] = self_user()
    except TokenExpiredError:
        refresh_token()
        session['user'] = self_user()
    except Exception:
        abort(500)


@ACCOUNT.route('me.json', methods=["GET"])
@is_auth
def me():
    refresh_user_session()
    return jsonify({'data': self_user()})


@ACCOUNT.route('me.html', methods=["GET"])
@is_auth
def me_view():
    refresh_user_session
    return render_template('account/me.html')


@ACCOUNT.route('logout', methods=["GET"])
@is_auth
def logout_me():
    logout()
    return "ok log out"
