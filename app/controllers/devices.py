# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from flask.json import jsonify
from app.voxity import get_devices, get_device
from app.controllers import is_auth
from app.voxity.objects import Device


DEVICES = Blueprint('DEVICES', __name__)


@DEVICES.route('', methods=["GET"])
@is_auth
def devices_json():
    data = get_devices()
    return jsonify({'data': data})


@DEVICES.route('view.html', methods=["GET"])
@is_auth
def devices():

    return render_template(
        'devices/index.html',
        devices=get_devices(ret_object=True, sort_by_extention=True)
    )


@DEVICES.route('<device_id>.json', methods=["GET"])
@DEVICES.route('', methods=["GET"])
def device_json(device_id):
    return jsonify({'data': get_device(device_id)})


@DEVICES.route('<device_id>.html', methods=["GET"])
@DEVICES.route('', methods=["GET"])
def device(device_id=None):
    return render_template(
        'devices/id.html',
        device=get_device(device_id, ret_object=True)
    )
