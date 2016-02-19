# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, session
from flask.json import jsonify
from app.voxity import get_devices, get_device, refresh_token


DEVICES = Blueprint('DEVICES', __name__)




@DEVICES.route('', methods=["GET"])
def devices_json():
    data = get_devices()
    return jsonify({'data': data})


@DEVICES.route('view.html', methods=["GET"])
def devices():

    data = get_devices()

    devices = list()
    for dev in data:
        devices.append(dev)

    devices = sorted(devices, key=lambda k: k['extension'])
    return render_template('devices/index.html', devices=devices, usr=session['user'])


@DEVICES.route('<device_id>', methods=["GET"])
@DEVICES.route('', methods=["GET"])
def device_json(device_id):
    return jsonify(get_device(device_id))


@DEVICES.route('<device_id>-veiw.html', methods=["GET"])
@DEVICES.route('', methods=["GET"])
def device(device_id=None):
    return render_template('devices/id.html', device=get_device(device_id), usr=session['user'])
