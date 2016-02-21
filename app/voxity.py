# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from requests_oauthlib import OAuth2Session
from flask import current_app, session
from datetime import datetime
voxity_bind = None


def connectors(**kwargs):
    now = datetime.now()
    token_expire_date = datetime.fromtimestamp(
        session['oauth_token']['expires_at']
    )
    token = kwargs.get('token', session['oauth_token'])

    if token_expire_date <= now:
        conn = OAuth2Session(current_app.config['CLIENT_ID'], token=token)
        session['oauth_token'] = conn.refresh_token(
            current_app.config['VOXITY']['request_token_url'],
            **{
                'client_id': current_app.config['CLIENT_ID'],
                'client_secret': current_app.config['CLIENT_SECRET']
            }
        )
        token = session['oauth_token']
    return OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=token
    )


def bind(**kwargs):
    return OAuth2Session(current_app.config['CLIENT_ID'], **kwargs)


def refresh_token():
    return connectors()


def pager_dict(headers):
    return {
        'total': headers.get('x-paging-total-records', None),
        'curent_page': headers.get('x-paging-page', 1),
        'max_page': headers.get('x-paging-total-pages', None)
    }

def get_devices():
    return connectors().get(
        current_app.config['BASE_URL'] + '/devices/'
    ).json()['data']


def get_device(d_id):
    return connectors().get(
        current_app.config['BASE_URL'] + '/devices/' + d_id
    ).json()['data']


def get_contacts(page=None, limit=None, name=None):
    if name:
        name = "*{0}*".format(name)
    resp = connectors().get(
        current_app.config['BASE_URL'] + '/contacts',
        params={
            'page': page,
            'limit': limit,
            'cn': name,
        }
    )
    data = {}
    data['list'] = resp.json()['result']
    data['pager'] = pager_dict(resp.headers)
    return data


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

    return resp


def get_calls_log(page=None, limit=None):
    resp = connectors().get(
        current_app.config['BASE_URL'] + '/calls/logs',
        params={
            'page': page,
            'limit': limit
        }
    )

    data = {}
    data['list'] = resp.json()['result']
    data['pager'] = pager_dict(resp.headers)

    return data
