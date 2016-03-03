# -*- coding: utf-8 -*-
"""Voxity api module."""
from __future__ import absolute_import, division, unicode_literals
from requests_oauthlib import OAuth2Session
from flask import current_app, session, abort
from datetime import datetime, timedelta
from app.utils import datetime_to_timestamp
from requests.models import Response
from app.voxity.objects import Device


def check_respons(resp):
    if isinstance(resp, Response):
        if resp.status_code >= 400:
            abort(resp.status_code)
        return True
    return False


def save_token(token):
    '''
    :param dict token: token object
    :retype: None
    '''
    token['expires_in'] = -3000
    token['expires_at'] = datetime_to_timestamp(
        datetime.now() + timedelta(days=7)
    )

    session['oauth_token'] = token
    session.modified = True


def bind(**kwargs):
    return OAuth2Session(current_app.config['CLIENT_ID'], **kwargs)


def connectors(**kwargs):
    """
    :param dict token: token dict, default = session[oauth_token]
    :retryp:OAuth2Session
    """
    token = kwargs.get('token', session.get('oauth_token', None))
    if isinstance(token, dict):
        return bind(token=token)
    else:
        return None


def pager_dict(headers):
    '''
    :param request.headers:
    :retype: dict
    :return: dict pagger from header response
    '''
    return {
        'total_item': headers.get('x-paging-total-records', None),
        'max_page': headers.get('x-paging-total-pages', None),
        'curent': headers.get('x-paging-page', 1),
        'next': headers.get('x-paging-next', None),
        'previous': headers.get('x-paging-previous', None),
        'limit': headers.get('x-paging-limit', None)
    }


def oauth_status():
    con = connectors()
    if con is not None:
        return con.get(
            current_app.config['BASE_URL'] + '/oauth/status'
        ).json()
    return None


def self_user():
    con = connectors()
    if con is not None:
        return con.get(
            current_app.config['BASE_URL'] + '/users/self'
        ).json()

    return None


def logout():
    con = connectors()
    if con is not None:
        resp = con.get(current_app.config['BASE_URL'] + "/logout")
        session['user'] = {}
        session['oauth_token'] = {}
        session['oauth_state'] = {}
        session.modified = True

        return resp

    return None
