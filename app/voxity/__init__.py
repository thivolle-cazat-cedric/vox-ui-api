# -*- coding: utf-8 -*-
"""Voxity api module."""
from __future__ import absolute_import, division, unicode_literals
from requests_oauthlib import OAuth2Session
from flask import current_app, session, abort
from datetime import datetime, timedelta
from app.utils import datetime_to_timestamp
from requests.models import Response
from app.voxity.error import ExceptVoxityTokenExpired


_DURATION_TOKEN = timedelta(days=7)


def check_respons(resp, esc_bad_resp=True):
    if isinstance(resp, Response):
        if resp.status_code == 401:
            session['try_refresh_token'] = 0
            session.modified = True
            raise ExceptVoxityTokenExpired()
        if esc_bad_resp and resp.status_code >= 400:
            abort(resp.status_code)
        if not esc_bad_resp and resp.status_code > 400:
            pass
        return True
    return False


def save_token(token):
    '''
    :param dict token: token object
    :retype: None
    '''
    token['expires_in'] = int(_DURATION_TOKEN.total_seconds())
    token['expires_at'] = datetime_to_timestamp(
        datetime.now() + _DURATION_TOKEN
    )
    session['oauth_token'] = token
    session['try_refresh_token'] = 0
    session['user'] = self_user()

    session.modified = True


def bind(**kwargs):
    return OAuth2Session(client_id=current_app.config['CLIENT_ID'], **kwargs)


def refresh_token():
    '''
    :retryp:OAuth2Session
    :return:valid conector
    '''
    vox_bind = bind(
        token=session['oauth_token']
    )
    token = vox_bind.refresh_token(
        current_app.config['TOKEN_URL'],
        client_id=current_app.config['CLIENT_ID'],
        client_secret=current_app.config['CLIENT_SECRET'],
        refresh_token=session['oauth_token']['refresh_token'],
    )
    save_token(token)

    return connectors()


def connectors(**kwargs):
    """
    :param dict token: token dict, default = session[oauth_token]
    :retryp:OAuth2Session
    """
    token = kwargs.get('token', session.get('oauth_token', None))
    if isinstance(token, dict):
        return bind(
            token=token,
            auto_refresh_url=current_app.config['TOKEN_URL'],
            auto_refresh_kwargs={
                'client_id': current_app.config['CLIENT_ID'],
                'client_secret': current_app.config['CLIENT_SECRET']
            }
        )
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
        try:
            return con.get(
                current_app.config['BASE_URL'] + '/oauth/status'
            ).json().get('message', 'unknow').lower()
        except Exception:
            pass

    return None


def self_user():
    con = connectors()
    if con is not None:
        resp = con.get(
            current_app.config['BASE_URL'] + '/users/self'
        )
        if check_respons(resp):
            return resp.json()['result']

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


def api_proxy(uri, method, params=None, data=None):
    method = method.lower()
    con = connectors()
    if uri and uri[0] != '/':
        uri = "/" + uri
    uri = current_app.config['BASE_URL'] + uri
    if con is None:
        return None

    if method == 'get':
        if params is not None and not isinstance(params, dict):
            raise ValueError('voxity.proxy : params must be a dict')
        resp = con.get(uri, params=params)

    return resp
