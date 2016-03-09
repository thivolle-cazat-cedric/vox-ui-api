# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import current_app
from . import connectors, check_respons, pager_dict
from .objects.channel import Channel


def get_base_url():
    return current_app.config['BASE_URL'] + '/channels/'

def create(exten):
    con = connectors()
    if con is not None:
        return con.post(
            get_base_url(),
            data={'exten': exten}
        ).json()

    return None

def get(ret_object=False, **kwargs):
    """
    :retyp: list
    :return: device list
    """

    con = connectors()
    if con:
        resp = con.get(get_base_url(), params=kwargs)
        if check_respons(resp):
            ret = resp.json().get('result', [])
            if not ret_object:
                return ret
            else:
                return Channel.litst_object_from_dict(ret, **kwargs)

    return None

def get_local_filter(ret_object=False, **kwargs):
    ret = list()
    if not kwargs:
        return get(ret_object=ret_object)
    else:
        channels = get()

    for c in channels:
        conditions = list()
        for k in kwargs.keys():
            if (kwargs[k].count('*') == 2 and
                kwargs[k][0] == '*' and
                kwargs[k][-1] == '*' and
                len(kwargs[k]) > 2):
                conditions.append(str(c[k]).lower() in str(kwargs[k]).lower())
            else:
                conditions.append(str(c[k]).lower() == str(kwargs[k]).lower())

        if any(conditions) and ret_object:
            c = Channel(**c)
            ret.append(c)
        elif any(conditions) and not ret_object:
            ret.append(c)

    return ret


def get_id(d_id, ret_object=False):
    """
    :param str d_ind: device id
    :retype: dict|Channel
    :return: one device
    """

    con = connectors()
    if con:
        resp = con.get(get_base_url() + d_id)
        if check_respons(resp):
            ret = resp.json().get('data', [])
            if not ret_object:
                return ret
            else:
                return Channel(**ret)
    return None

def get_log(**kwargs):
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