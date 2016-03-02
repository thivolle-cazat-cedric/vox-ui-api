# -*- coding: utf-8 -*-
from __future__ import (
    absolute_import, division, print_function, unicode_literals
)
from flask import (
    Flask, request, session, url_for, redirect, abort,
    render_template
)
from datetime import datetime

from app.config import config_loader
from app import controllers, voxity


__VERSION__ = "1.0.0α"


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

    app.config['__VERSION__'] = __VERSION__

    @app.route("/")
    def index():
        """Step 1: User Authorization.
        Redirect the user/resource owner to the OAuth provider (i.e. Github)
        using an URL with a few key OAuth parameters.
        """

        if controllers.valide_session() and voxity.connectors() is not None:
            return redirect(url_for('DEVICES.devices'))

        try:
            voxity.logout()
        except Exception:
            controllers.clear_session()

        return redirect(url_for('ACCOUNT.signin'))

    @app.route("/favicon.ico")
    def favicon():
        return redirect(url_for('static', filename='icon/fav/vox-ui-api.ico'))

    @app.route("/callback", methods=["GET"])
    def callback():
        """
        Step 3: Retrieving an access token.
        The user has been redirected back from the provider to your registered
        callback URL. With this redirection comes an authorization code included
        in the redirect URL. We will use that to obtain an access token.
        """

        voxity_bind = voxity.bind(
            redirect_uri=app.config['REDIRECT_URI']
        )
        voxity.save_token(voxity_bind.fetch_token(
            app.config['TOKEN_URL'],
            client_secret=app.config['CLIENT_SECRET'],
            authorization_response=request.url
        ))

        return redirect(url_for('DEVICES.devices'))

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
        def err_except_all(error):
            app.logger.error(
                "{0} ERROR 500 : {1}".format("#" * 10, error),
                exc_info=error
            )
            return render_template(
                'err/500.html',
                error_code='500',
                error_icon="#x1f632",
                link_to_home=True,
            ), 500

        @app.errorhandler(500)
        def err_500_all(err):
            app.logger.error(
                "{0} ERROR 500 : {1}".format("#" * 10, err),
                exc_info=err
            )
            return render_template(
                'err/500.html',
                error_code='500',
                error_icon="#x1f632",
                link_to_home=True,
            ), 500

    else:
        @app.route("/err/<int:error>", methods=["GET"])
        def raise_error(error):
            abort(error)

        @app.route("/debug/oauth_info")
        def show_oath():
            expired = datetime.fromtimestamp(
                session['oauth_token']['expires_at']
            )
            return """
            token :{0}<br>
            expired : {1}
            """.format(
                session['oauth_token'],
                expired
            )

        @app.route("/debug/raise")
        def raise_exception():
            raise Exception

    return app
