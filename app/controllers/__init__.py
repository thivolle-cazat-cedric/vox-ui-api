# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from functools import wraps
from flask import session, url_for, redirect, abort
from app.voxity import token_is_expired


def is_auth(function):
    @wraps(function)
    def try_is_authenticate(*args, **kwargs):
        '''
        Verifie si la requette provient d'une personne authentifier.
        Pour savoir si il est authentifier, il doit avoir en variable de \
        session :
            * *(boom)*status = ``True``
        '''

        if 'oauth_token' not in session:
            return redirect(url_for('index'))

        if 'access_token' not in session['oauth_token']:
            try:
                if token_is_expired():
                    return redirect(url_for('index'))
            except Exception:
                return redirect(url_for('index'))

        return function(*args, **kwargs)

    return try_is_authenticate

from app.controllers.devices import DEVICES
from app.controllers.contacts import CONTACT
from app.controllers.calls import CALLS
from app.controllers.account import ACCOUNT
from app.controllers.calls_log import CALLS_LOG