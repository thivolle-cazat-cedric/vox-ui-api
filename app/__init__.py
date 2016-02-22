# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from flask import Flask, request, session, url_for, redirect, abort, render_template
from flask_oauthlib.client import OAuth
from datetime import datetime

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

    @app.route("/raise")
    def show_raise():
        raise Exception

    @app.route("/")
    def index():
        """Step 1: User Authorization.
        Redirect the user/resource owner to the OAuth provider (i.e. Github)
        using an URL with a few key OAuth parameters.
        """

        # try:
        #     if voxity.connectors():
        #         return redirect(url_for('DEVICES.devices'))
        # except:
        #     controllers.clear_session()

        return redirect(url_for('ACCOUNT.signin'))


    @app.route("/callback", methods=["GET"])
    def callback():
        """ Step 3: Retrieving an access token.
        The user has been redirected back from the provider to your registered
        callback URL. With this redirection comes an authorization code included
        in the redirect URL. We will use that to obtain an access token.
        """

        voxity_bind = voxity.bind(
            state=session['oauth_state'],
            redirect_uri=app.config['REDIRECT_URI']
        )
        token = voxity_bind.fetch_token(
            app.config['TOKEN_URL'],
            client_secret=app.config['CLIENT_SECRET'],
            authorization_response=request.url
        )

        voxity.save_token(token)
        session['user'] = voxity.self_user()

        return redirect(url_for('DEVICES.devices', **{'direction': 'incoming'}))


    @app.route("/err/500", methods=["GET"])
    def raise_error_500():
        abort(500)

    @app.errorhandler(500)
    def err_500(e):
        return render_template('err/500.html'), 500


    @app.route("/err/404", methods=["GET"])
    def raise_error_404():
        abort(404)

    @app.errorhandler(404)
    def err_404(e):
        return render_template('err/404.html'), 404


    if not app.config['DEBUG']:
        @app.errorhandler(Exception)
        def err_500_all(e):
            return render_template('err/500.html'), 500
    else:
        @app.route("/oauth_info")
        def show_oath():
            expired = datetime.fromtimestamp(session['oauth_token']['expires_at'])
            return """
            state : {0}<br>
            token :{1}<br>
            expired at : {2}
            """.format(
                session['oauth_state'],
                session['oauth_token'],
                expired
            )

    return app
