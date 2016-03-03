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
                data['list'] = Contact.litst_object_from_dict(resp.json()['result'])
            else:
                data['list'] = resp.json()['result']
            return data

        return None


def get_uid(ret_object=False, uid=None):
    """
    :retyp: dict|Contact
    """

    con = connectors()
    if con is not None:
        resp = con.get(get_base_url() + uid)
        if check_respons(resp):
            if ret_object:
                return Contact.litst_object_from_dict(resp.json()['result'])
            else:
                return resp.json()['result']

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
