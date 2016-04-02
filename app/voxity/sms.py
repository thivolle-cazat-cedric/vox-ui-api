# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import current_app
from .objects.sms import Sms
from . import connectors, check_respons

SAMPLES = """{
    "status" : 200,
    "result" : [
        {
            "id": "sm2372e390-da57-11e5-a15e-a711cf0e9b38",
            "client_id": "mbEPthtkUbzr2Lrn2dzc",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 17:59:09",
            "phone_number": "+33666951941",
            "emitter": "Voxity",
            "content": "Hello world !",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-23 17:59:18",
            "id_retour": "87845418",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "SFR",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm298fd7c0-da5b-11e5-ade5-91f1ab0e1da5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 18:27:57",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "Coucou copain !",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-23 18:28:07",
            "id_retour": "87850564",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm32a387c0-e515-11e5-8ab7-dbc2cc6be7c5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-03-08 10:04:51",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "hh",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-03-08 10:06:23",
            "id_retour": "89544472",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm34240120-daec-11e5-9ce2-cfe706823845",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-24 11:46:12",
            "phone_number": "+33666951941",
            "emitter":null,
            "content": "rfkjhrfglkrfgkyugfljsrgfelgfkjrhflkjdgltgkujgfrylu...",
            "nb_sms": "2",
            "status": "DELIVERED",
            "delivery_date": "2016-02-24 11:46:22",
            "id_retour": "87892930",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "SFR",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm40162070-da57-11e5-ade5-91f1ab0e1da5",
            "client_id": "mbEPthtkUbzr2Lrn2dzc",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 17:59:57",
            "phone_number": "+33618635768",
            "emitter": "Voxity",
            "content": "Hello world !",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-23 18:00:10",
            "id_retour": "87845429",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm5cf8eec0-e515-11e5-8ab7-dbc2cc6be7c5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-03-08 10:06:02",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "dd",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-03-08 10:05:54",
            "id_retour": "89547129",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm6dce1490-da71-11e5-ade5-91f1ab0e1da5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 21:07:21",
            "phone_number": "+33611223344",
            "emitter":null,
            "content": "Bonjour",
            "nb_sms": "1",
            "status": "ERROR",
            "delivery_date":null,
            "id_retour":null,
            "code": "24",
            "code_message": "No commercial sending between 8PM and 8AM, neither...",
            "statut":null,
            "libelle":null,
            "operateur":null,
            "code_erreur":null,
            "deleted": "0"
        },
        {
            "id": "sm7139ee20-da57-11e5-ade5-91f1ab0e1da5",
            "client_id": "mbEPthtkUbzr2Lrn2dzc",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 18:01:20",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "Hello world !",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-23 18:01:29",
            "id_retour": "87845485",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm906c1400-daeb-11e5-9ce2-cfe706823845",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-24 11:41:37",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "ddd",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-24 11:41:48",
            "id_retour": "87892858",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "smb9ec0300-da71-11e5-ade5-91f1ab0e1da5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 21:09:29",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "cdd",
            "nb_sms": "1",
            "status": "ERROR",
            "delivery_date":null,
            "id_retour":null,
            "code": "24",
            "code_message": "No commercial sending between 8PM and 8AM, neither...",
            "statut":null,
            "libelle":null,
            "operateur":null,
            "code_erreur":null,
            "deleted": "0"
        },
        {
            "id": "smcdbe49e0-da5a-11e5-ade5-91f1ab0e1da5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-23 18:25:23",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "test",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-23 18:25:37",
            "id_retour": "87850550",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "smd3b57c30-e557-11e5-8ab7-dbc2cc6be7c5",
            "client_id": "rTSMIRphY5mJKhF3FfVf",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-03-08 18:01:48",
            "phone_number": "+33618635768",
            "emitter": "Voxity",
            "content": "Hello world !",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-03-08 18:01:57",
            "id_retour": "89631853",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "smda829bb0-dad5-11e5-a77d-513ed2cf0e92",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-02-24 09:06:13",
            "phone_number": "+33618635768",
            "emitter":null,
            "content": "test",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-02-24 09:06:25",
            "id_retour": "87873224",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        },
        {
            "id": "sm0c650890-e515-11e5-8ab7-dbc2cc6be7c5",
            "client_id": "3VT8fh7jPfpR6sxN4N2z",
            "client_octo_id": "v009",
            "user_id": "1",
            "send_date": "2016-03-08 10:03:46",
            "phone_number": "+33618635768",
            "emitter": null,
            "content": "ee",
            "nb_sms": "1",
            "status": "DELIVERED",
            "delivery_date": "2016-03-08 10:06:17",
            "id_retour": "89540016",
            "code": "0",
            "code_message": "Your message has been sent",
            "statut": "0",
            "libelle": "SMS remis",
            "operateur": "ORAN",
            "code_erreur": "000",
            "deleted": "0"
        }
    ]
}"""


def get_base_url():
    return current_app.config['BASE_URL'] + '/sms/'


def get(ret_object=False):
    """
    :retyp: list
    :return: device list
    """

    con = connectors()
    if con:
        resp = con.get(get_base_url())
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
            get_base_url(),
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
