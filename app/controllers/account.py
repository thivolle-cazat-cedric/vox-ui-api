# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from oauthlib.oauth2 import TokenExpiredError
from flask import Blueprint, render_template, session, abort, current_app, redirect, request
from flask.json import jsonify
from app.voxity import self_user, logout, bind, oauth_status
from app.controllers import is_auth, clear_session


ACCOUNT = Blueprint('ACCOUNT', __name__)
LIST_AVAILABLE = [5, 10, 25, 50, 100]


def refresh_user_session():
    try:
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
    refresh_user_session()
    return render_template('account/me.html')

@ACCOUNT.route('settings/notify.html', methods=["GET"])
def settings_notify():
    refresh_user_session()
    return render_template(
        'account/notify.html',
        container_class='container-fluid'
    )


@ACCOUNT.route('status.json', methods=["GET"])
def get_oauth_status():
    return jsonify({'data': oauth_status()})

@ACCOUNT.route('logout', methods=["GET"])
def logout_me():
    try:
        logout()
    except Exception:
        pass
    clear_session()
    return "ok log out"


@ACCOUNT.route('signin', methods=["GET"])
def signin():
    clear_session()

    if request.args.get('next', False):
        session['next_uri_aft_signin'] = request.args['next']
        session.modified = True

    voxity_bind = bind(redirect_uri=current_app.config['REDIRECT_URI'])
    authorization_url, state = voxity_bind.authorization_url(
        current_app.config['AUTHORIZATION_BASE_URL']
    )
    session['authorization_url'] = authorization_url
    return redirect(authorization_url)
