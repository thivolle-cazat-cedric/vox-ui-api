# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from flask import Flask, request, session, url_for, redirect, abort, render_template
from flask_oauthlib.client import OAuth

from app.config import config_loader
from app import controllers
from app import voxity

oauth = OAuth()


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
    oauth.init_app(app)

    app.register_blueprint(
        controllers.DEVICES,
        url_prefix='/devices/'
    )
    app.register_blueprint(
        controllers.CONTACT,
        url_prefix='/contacts/'
    )

    app.register_blueprint(
        controllers.CALLS,
        url_prefix='/calls/'
    )
    app.register_blueprint(
        controllers.ACCOUNT,
        url_prefix='/account/'
    )
    app.register_blueprint(
        controllers.CALLS_LOG,
        url_prefix='/call_log/'
    )

    @app.route("/")
    def index():
        """Step 1: User Authorization.
        Redirect the user/resource owner to the OAuth provider (i.e. Github)
        using an URL with a few key OAuth parameters.
        """
        voxity_bind = voxity.bind(
            app.config['CLIENT_ID'],
            redirect_uri=app.config['REDIRECT_URI']
        )
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

        voxity_bind = voxity.bind(
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

        conn = voxity.connectors(
            app.config['CLIENT_ID'],
            session['oauth_token']
        )
        session['user'] = voxity.self_user()

        return redirect(url_for('DEVICES.devices'))


    @app.route("/err/500", methods=["GET"])
    def raise_error_500():
        abort(500)

    @app.errorhandler(500)
    def err_500(e):
        return render_template('err/500.html'), 500

    if not app.config['DEBUG']:
        @app.errorhandler(Exception)
        def err_500_all(e):
            return render_template('err/500.html'), 500

    @app.route("/err/404", methods=["GET"])
    def raise_error_404():
        abort(404)

    @app.errorhandler(404)
    def err_404(e):
        return render_template('err/404.html'), 404

    return app
