# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from flask import Flask, request, session, url_for, redirect
from requests_oauthlib import OAuth2Session

from app.config import config_loader
from app.controllers.devices import DEVICES
from app.controllers.contacts import CONTACT
from app.controllers.calls import CALLS
from app.voxity import voxity_bind


def create_app(env='prod'):
    """
    Initialise l'application (configuration, blueprints, base de données, ...)

    :param str env: le nom de l'environement (dev, prod, tests, ...)

    :return: l'application initilisée
    :rtype: flask.Flask
    """
    app = Flask(
        'vox_peer',
        template_folder="app/templates",
        static_folder="app/lib"
    )
    config_loader(app.config, env)
    voxity_bind = OAuth2Session(
        app.config['CLIENT_ID'],
        redirect_uri=app.config['REDIRECT_URI']
    )
    app.register_blueprint(
        DEVICES,
        url_prefix='/devices/'
    )
    app.register_blueprint(
        CONTACT,
        url_prefix='/contacts/'
    )

    app.register_blueprint(
        CALLS,
        url_prefix='/calls/'
    )

    @app.route("/")
    def index():
        """Step 1: User Authorization.
        Redirect the user/resource owner to the OAuth provider (i.e. Github)
        using an URL with a few key OAuth parameters.
        """
        authorization_url, state = voxity_bind.authorization_url(
            app.config['AUTHORIZATION_BASE_URL']
        )
        session['oauth_state'] = state
        return redirect(authorization_url)

    @app.route("/callback", methods=["GET"])
    def callback():
        """ Step 3: Retrieving an access token.
        The user has been redirected back from the provider to your registered
        callback URL. With this redirection comes an authorization code included
        in the redirect URL. We will use that to obtain an access token.
        """

        voxity_bind = OAuth2Session(
            app.config['CLIENT_ID'],
            state=session['oauth_state'],
            redirect_uri=app.config['REDIRECT_URI']
        )
        token = voxity_bind.fetch_token(
            app.config['TOKEN_URL'],
            client_secret=app.config['CLIENT_SECRET'],
            authorization_response=request.url
        )
        session['oauth_token'] = token

        voxity = OAuth2Session(
            app.config['CLIENT_ID'],
            token=session['oauth_token']
        )
        session['user'] = voxity.get(app.config['BASE_URL'] + '/users/self').json()
        print(url_for('DEVICES.devices'))
        return redirect(url_for('DEVICES.devices'))

    return app
