from requests_oauthlib import OAuth2Session
from flask import current_app, session

voxity_bind = None

def get_devices():
    voxity = OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=session['oauth_token']
    )
    return voxity.get(
        current_app.config['BASE_URL'] + '/devices/'
    ).json()['data']

def get_device(d_id):
    voxity = OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=session['oauth_token']
    )
    return voxity.get(
        current_app.config['BASE_URL'] + '/devices/' + d_id
    ).json()['data']

def get_contacts():
    voxity = OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=session['oauth_token']
    )
    return voxity.get(
        current_app.config['BASE_URL'] + '/contacts'
    ).json()['result']

def call(exten):
    voxity = OAuth2Session(
        current_app.config['CLIENT_ID'],
        token=session['oauth_token']
    )
    return voxity.post(
        current_app.config['BASE_URL'] + '/channels/',
        data={'exten': exten}
    ).json()
