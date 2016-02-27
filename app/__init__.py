# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from traceback import print_exception
from sys import exc_info
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
        try:
            voxity.logout()
        except Exception:
            pass
        controllers.clear_session()
        return redirect(url_for('ACCOUNT.signin'))

    @app.route("/callback", methods=["GET"])
    def callback():
        """ Step 3: Retrieving an access token.
        The user has been redirected back from the provider to your registered
        callback URL. With this redirection comes an authorization code included
        in the redirect URL. We will use that to obtain an access token.
        """

        controllers.clear_session()
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

        return redirect(url_for('DEVICES.devices', **{'direction': 'incoming'}))

    @app.route("/err/<int:error>", methods=["GET"])
    def raise_error(error):
        abort(error)

    @app.errorhandler(401)
    def err_401(e):
        return render_template(
            'err/401.html',
            error_code='401',
            error_icon="#128274",
            link_to_home=False,
        ), 401

    @app.errorhandler(403)
    def err_403(e):
        return render_template(
            'err/403.html',
            error_code='403',
            error_icon="#128274",
            link_to_home=False,
        ), 401

    @app.errorhandler(404)
    def err_404(e):
        return render_template(
            'err/404.html',
            error_code='404',
            error_icon="#x1F47B",
            link_to_home=True,
        ), 404

    if not app.config['DEBUG']:
        @app.errorhandler(Exception)
        def err_500_all(e):
            app.logger.error(print_exc(limit=8))
            return render_template(
                'err/500.html',
                error_code='500',
                error_icon="#x1f632",
                link_to_home=True,
            ), 500
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
