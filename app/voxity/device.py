# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import current_app
from .objects.devices import Device
from . import connectors, check_respons


def get_base_url():
    return current_app.config['BASE_URL'] + '/devices/'


def get(ret_object=False, **kwargs):
    """
    :retyp: list
    :return: device list
    """

    con = connectors()
    if con:
        resp = con.get(get_base_url(), params={'details': 'true'})
        if check_respons(resp):
            ret = resp.json().get('data', [])
            devices = Device.litst_obj_from_list(ret, **kwargs)
            if not ret_object:
                ret = list()
                for d in devices:
                    ret.append(d.to_dict())
                return ret
            else:
                return devices

    return None


def get_id(d_id, ret_object=False):
    """
    :param str d_ind: device id
    :retype: dict
    :return: one device
    """

    con = connectors()
    if con:
        resp = con.get(get_base_url() + d_id, params={'details': 'true'})
        if check_respons(resp):
            ret = resp.json().get('data', [])
            if not ret_object:
                return ret
            else:
                return Device(**ret)
    return None
