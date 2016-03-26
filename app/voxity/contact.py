# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import current_app
from . import connectors, check_respons, pager_dict
from .objects.contact import Contact


def get_base_url():
    return current_app.config['BASE_URL'] + '/contacts/'


def get(ret_object=False, **kwargs):
    """
    :retyp: dict
    :return: {
        'pagger' : dict() about page
        'list' : contact list (dict|Contact object)
    }
    """

    if 'cn' in kwargs:
        kwargs['cn'] = "*{0}*".format(kwargs['cn'])

    con = connectors()
    if con is not None:
        resp = con.get(get_base_url(), params=kwargs)
        if check_respons(resp):
            data = {}
            data['pager'] = pager_dict(resp.headers)
            if ret_object:
                data['list'] = Contact.litst_obj_from_list(resp.json()['result'])
            else:
                data['list'] = resp.json()['result']
            return data

        return None


def get_uid(uid=None, ret_object=False):
    """
    :retyp: dict|Contact
    """

    con = connectors()
    if con is not None:
        resp = con.get(get_base_url() + uid)
        if check_respons(resp):
            try:
                if ret_object:
                    return Contact(**resp.json()['result'][0])
                else:
                    return resp.json()['result'][0]
            except Exception:
                return None
    return None


def add(**kwargs):
    kwargs.pop('uid', None)

    for k in kwargs.keys():
        if not kwargs[k]:
            kwargs.pop(k, None)

    con = connectors()
    if con is not None:
        resp = con.post(
            get_base_url(),
            json=kwargs,
            headers={'Content-Type': 'application/json'}
        )
        if check_respons(resp, esc_bad_resp=False):
            return resp.json()

    return {'errors': {'no_response': 'unexpended error'}}


def update(**kwargs):
    if not 'uid' in kwargs:
        raise ValueError('contact.update : args [uid] is missing')

    con = connectors()
    if con is not None:
        resp = con.put(
            get_base_url() + kwargs.pop('uid'),
            json=kwargs,
            headers={'Content-Type': 'application/json'}
        )
        if check_respons(resp, esc_bad_resp=False):
            return resp.json()

    return {'errors': {'no_response': 'unexpended error'}}
