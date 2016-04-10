# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import current_app
from .objects.sms import Sms, SmsRespons
from . import connectors, check_respons


def get_url(additional=None):
    ret = current_app.config['BASE_URL'] + '/sms/'
    if additional:
        ret += additional

    return ret


def get(ret_object=False):
    """
    :retyp: list
    :return: device list
    """

    con = connectors()
    if con:
        resp = con.get(get_url())
        if check_respons(resp):
            print(resp.text)
            ret = resp.json().get('result', [])
            sms_list = Sms.litst_obj_from_list(ret)
            if not ret_object:
                ret = list()
                for s in sms_list:
                    ret.append(s.to_dict())
                return ret
            else:
                return sms_list

    return None


def get_group_by_dest(ret_object=False, **kwargs):
    sms_list = get(ret_object=True)
    if sms_list:
        ret = {}
        for s in sms_list:
            if s.phone_number not in ret:
                ret[s.phone_number] = []
            if ret_object:
                ret[s.phone_number].append(s)
            else:
                ret[s.phone_number].append(s.to_dict())
        return ret
    else:
        return None


def send(message):
    if isinstance(message, Sms):
        message = message.to_dict()
    elif isinstance(message, dict):
        raise ValueError('sms.send : arg1 must be sms instance or dict representation')

    con = connectors()
    data = {}
    data['phone_number'] = message['phone_number']
    data['content'] = message['content']
    data['emitter'] = message['emitter']

    if con is not None:
        resp = con.post(
            get_url(),
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        if check_respons(resp, esc_bad_resp=False) and resp.status_code == 200:
            message = resp.json().get('result', None)
            if message is not None:
                return Sms(**message)
            else:
                return Sms(**message)

    return None


def get_responses(ret_object=False, **kwargs):
    con = connectors()
    if con is not None:
        resp = con.get(get_url('responses'))

        if check_respons(resp):
            responses = resp.json().get('result', None)
            ret = []
            if responses:
                for response in responses:
                    response = SmsRespons(**response)
                    if ret_object:
                        ret.append(response)
                    else:
                        ret.append(response.to_dict())
            return ret

    return None
