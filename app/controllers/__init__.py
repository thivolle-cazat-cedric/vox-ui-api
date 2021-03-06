# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from functools import wraps
from flask import session, abort
from app.voxity import self_user


def clear_session():
    for k in ['authorization_url', 'oauth_state', 'oauth_token', 'user']:
        session.pop(k, None)
    session.modified = True

def valide_session():
    return (
        'oauth_token' in session and
        'access_token' in session['oauth_token']
    )


def is_auth(function):
    @wraps(function)
    def try_is_authenticate(*args, **kwargs):
        '''
        Verifie si la requette provient d'une personne authentifier.
        Pour savoir si il est authentifier, il doit avoir en variable de \
        session :
            * *(boom)*status = ``True``
        '''

        if not valide_session():
            clear_session()
            abort(401)

        if not session.get('user', False):
            session['user'] = self_user()

        return function(*args, **kwargs)
    return try_is_authenticate


def is_admin(function):
    @wraps(function)
    def is_adm(*args, **kwargs):
        if not isinstance(session.get('user', None), dict):
            abort(401)

        if not session['user'].get('is_admin', False):
            abort(403)

        return function(*args, **kwargs)
    return is_adm

from app.controllers.devices import DEVICES
from app.controllers.contacts import CONTACT
from app.controllers.calls import CALLS
from app.controllers.account import ACCOUNT
from app.controllers.calls_log import CALLS_LOG
from app.controllers.sms import SMS
from app.controllers.api_proxy import API_PROXY
