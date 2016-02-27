# -*- coding: utf-8 -*-
"""Voxity api module."""
from __future__ import absolute_import, division, unicode_literals
from requests_oauthlib import OAuth2Session
from flask import current_app, session
from datetime import datetime, timedelta
from app.utils import datetime_to_timestamp
voxity_bind = None


def token_is_expired(**kwargs):
    """
    :param dict token: *optional* token object, default, the session token
    :return: true if token is expired
    :retype: bool
    """

    return True
    token_expire_date = datetime.fromtimestamp(
        kwargs.get('token', session['oauth_token']['expires_at'])
    )

    return token_expire_date <= datetime.now()


def save_token(token):
    '''
    :param dict token: token object
    :retype: None
    '''
    token['expires_in'] = -300
    session['oauth_token'] = token
    session['oauth_at'] = None
    session.modified = True


def refresh_token():
    '''
    :retryp:OAuth2Session
    :return:valid conector
    '''
    conn = OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=session['oauth_token']
    )
    save_token(
        conn.refresh_token(
            current_app.config['TOKEN_URL'],
            client_id=current_app.config['CLIENT_ID'],
            client_secret=current_app.config['CLIENT_SECRET']
        )
    )
    return conn


def connectors(**kwargs):
    """
    :retryp:OAuth2Session
    """
    token = kwargs.get('token', session['oauth_token'])

    if session.get('user', False) and token_is_expired():
        return refresh_token()

    return OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=token,
    )


def bind(**kwargs):
    return OAuth2Session(current_app.config['CLIENT_ID'], **kwargs)


def pager_dict(headers):
    return {
        'total': headers.get('x-paging-total-records', None),
        'curent_page': headers.get('x-paging-page', 1),
        'max_page': headers.get('x-paging-total-pages', None)
    }


def get_devices():
    """
    :retyp: list
    :return: device list
    """
    return connectors().get(
        current_app.config['BASE_URL'] + '/devices/'
    ).json()['data']


def get_device(d_id):
    """
    :param str d_ind: device id
    :retype: dict
    :return: one device
    """
    return connectors().get(
        current_app.config['BASE_URL'] + '/devices/' + d_id
    ).json()['data']


def get_contacts(**kwargs):
    """
    :param int page: page number *default None*
    :param int limit: limit contact in response *default None*
    :param str name: name filter
    :retype: list
    :return: contact list
    """
    if 'cn' in kwargs:
        kwargs['cn'] = "*{0}*".format(kwargs['cn'])
    resp = connectors().get(
        current_app.config['BASE_URL'] + '/contacts/',
        params=kwargs
    )
    data = {}
    data['list'] = resp.json()['result']
    data['pager'] = pager_dict(resp.headers)
    return data


def add_contacts(**kwargs):
    """
    :param str cn: name **mandatory**
    :param str telephoneNumber: first phone number **mandatory**
    :param str mobile: mobile phone number
    :param str mail: mail adresse
    :retype: list
    :return: contact list
    """
    try:
        return connectors().post(
            current_app.config['BASE_URL'] + '/contacts/',
            params=kwargs
        ).json()
    except Exception:
        return None


def call(exten):
    return connectors().post(
        current_app.config['BASE_URL'] + '/channels',
        data={'exten': exten}
    ).json()


def self_user():
    return connectors().get(
        current_app.config['BASE_URL'] + '/users/self'
    ).json()

def logout():
    resp = connectors().get(current_app.config['BASE_URL'] + "/logout")
    session['user'] = {}
    session['oauth_token'] = {}
    session['oauth_state'] = {}
    session.modified = True

    return resp


def get_calls_log(**kwargs):
    resp = connectors().get(
        current_app.config['BASE_URL'] + '/calls/logs',
        params=kwargs
    )

    data = {}
    data['list'] = resp.json()['result']
    data['pager'] = pager_dict(resp.headers)

    return data
