# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, session, abort, current_app, redirect, request, url_for
from flask.json import jsonify
from app.voxity import self_user, logout, bind, oauth_status, save_token
from app.controllers import is_auth, clear_session, valide_session


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
    return redirect(url_for('PUBLIC.index'))


@ACCOUNT.route('signin-check', methods=["GET"])
def signin_check():
    if valide_session():
        oauth_s = oauth_status()
        if oauth_s and oauth_status == 'authenticated':
            return redirect(request.args.get('next', 'DEVICES.devices_view'))
        else:
            return redirect(url_for('ACCOUNT.signin'))
    else:
        return redirect(url_for('ACCOUNT.signin'))


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


@ACCOUNT.route("signin-callback", methods=["GET"])
def callback():
    """
    Step 3: Retrieving an access token.
    The user has been redirected back from the provider to your registered
    callback URL. With this redirection comes an authorization code included
    in the redirect URL. We will use that to obtain an access token.
    """

    voxity_bind = bind(
        redirect_uri=current_app.config['REDIRECT_URI']
    )
    save_token(voxity_bind.fetch_token(
        current_app.config['TOKEN_URL'],
        client_secret=current_app.config['CLIENT_SECRET'],
        authorization_response=request.url
    ))
    if 'next_uri_aft_signin' in session:
        return redirect(session.pop('next_uri_aft_signin'))
    else:
        return redirect(url_for('DEVICES.devices_view'))
