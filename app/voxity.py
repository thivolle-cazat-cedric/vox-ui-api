# -*- coding: utf-8 -*-
"""Voxity api module."""
from __future__ import absolute_import, division, unicode_literals
from requests_oauthlib import OAuth2Session
from flask import current_app, session
from datetime import datetime, timedelta
from app.utils import datetime_to_timestamp
voxity_bind = None


def save_token(token):
    '''
    :param dict token: token object
    :retype: None
    '''
    token['expires_in'] = -300
    token.pop('oauth_state', None)
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
    print(type(headers))
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


def get_devices():
    """
    :retyp: list
    :return: device list
    """
    con = connectors()
    if con:
        resp = con.get(
            current_app.config['BASE_URL'] + '/devices/'
        )
        return resp.json().get('data', [])

    return None


def get_device(d_id):
    """
    :param str d_ind: device id
    :retype: dict
    :return: one device
    """
    con = connectors()
    if con:
        return con.get(
            current_app.config['BASE_URL'] + '/devices/' + d_id
        ).json()['data']

    return None


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
    con = connectors()
    if con is not None:
        resp = con.get(
            current_app.config['BASE_URL'] + '/contacts/',
            params=kwargs
        )
        print('#'*20)
        print(type(resp))
        data = {}
        data['list'] = resp.json()['result']
        data['pager'] = pager_dict(resp.headers)
        return data

    return None


def add_contacts(**kwargs):
    """
    :param str cn: name **mandatory**
    :param str telephoneNumber: first phone number **mandatory**
    :param str mobile: mobile phone number
    :param str mail: mail adresse
    :retype: list
    :return: contact list
    """
    con = connectors()
    if con is not None:
        return con.post(
            current_app.config['BASE_URL'] + '/contacts/',
            params=kwargs
        ).json()

    return None


def call(exten):
    con = connectors()
    if con is not None:
        return con.post(
            current_app.config['BASE_URL'] + '/channels',
            data={'exten': exten}
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


def get_calls_log(**kwargs):
    con = connectors()
    if con is not None:
        resp = connectors().get(
            current_app.config['BASE_URL'] + '/calls/logs',
            params=kwargs
        )

        data = {}
        data['list'] = resp.json()['result']
        data['pager'] = pager_dict(resp.headers)

        return data

    return None
