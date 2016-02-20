from requests_oauthlib import OAuth2Session
from flask import current_app, session

voxity_bind = None


def connectors(client_id, token):
    conn = OAuth2Session(
        client_id,
        token=token
    )

    return conn


def bind(client_id, **kwargs):
    return OAuth2Session(client_id, **kwargs)


def refresh_token():
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])

    session['oauth_token'] = conn.refresh_token(
        current_app.config['VOXITY']['request_token_url'],
        **{
            'client_id': current_app.config['CLIENT_ID'],
            'client_secret': current_app.config['CLIENT_SECRET']
        }
    )


def pager_dict(headers):
    return {
        'total': headers.get('x-paging-total-records', None),
        'curent_page': headers.get('x-paging-page', 1),
        'max_page': headers.get('x-paging-total-pages', None)
    }

def get_devices():
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])
    return conn.get(
        current_app.config['BASE_URL'] + '/devices/'
    ).json()['data']


def get_device(d_id):
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])
    return conn.get(
        current_app.config['BASE_URL'] + '/devices/' + d_id
    ).json()['data']


def get_contacts(page=None, limit=None):
    conn = current_app.config['BASE_URL'] + '/logout'(current_app.config['CLIENT_ID'], session['oauth_token'])
    resp = conn.get(
        current_app.config['BASE_URL'] + '/contacts',
        params={
            'page': page,
            'limit': limit
        }
    )
    data = {}
    data['list'] = resp.json()['result']
    data['pager'] = pager_dict(resp.headers)
    return data


def call(exten):
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])
    resp = conn.post(
        current_app.config['BASE_URL'] + '/channels',
        data={'exten': exten}
    )
    return resp.json()


def self_user():
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])
    return conn.get(
        current_app.config['BASE_URL'] + '/users/self'
    ).json()


def logout():
    conn = connectors(current_app.config['CLIENT_ID'], session['oauth_token'])
    resp = conn.get("https://api.voxity.fr/api/v1/logout")
    session['user'] = {}
    session['oauth_token'] = ""
    return resp
