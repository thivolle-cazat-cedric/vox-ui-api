# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, abort
from flask.json import jsonify
from app.voxity import device, channel
from app.controllers import is_auth
from app.utils import roundup


DEVICES = Blueprint('DEVICES',
    __name__,
    template_folder='templates',
    url_prefix='/devices/',
    static_folder='static'
)


@DEVICES.route('index.html', methods=["GET"])
@is_auth
def index():
    item_per_lst = 4
    devices = device.get(ret_object=True, sort_by_extention=True)
    total_devices = len(devices)
    col = roundup(total_devices / item_per_lst)
    if col >= 4:
        item_per_lst = roundup(total_devices / 3)
        col = 3

    if col == 1:
        container_class = 'container'
    else:
        container_class = 'container-fluid'

    return render_template(
        'devices/index.html',
        container_class=container_class,
        col_length=col,
        item_per_lst=item_per_lst,
        devices=devices
    )


@DEVICES.route('index.json', methods=["GET"])
@is_auth
def devices_json():
    return jsonify({'data': device.get()})


@DEVICES.route('<device_id>.html', methods=["GET"])
@is_auth
def device_view(device_id=None):
    d = device.get_id(device_id, ret_object=True)

    return render_template(
        'devices/id.html',
        container_class='container-fluid',
        device=d,
        calls=channel.get_local_filter(ret_object=True, exten=d.extension)
    )


@DEVICES.route('<device_id>.json', methods=["GET"])
@is_auth
def device_json(device_id):

    return jsonify({'data': device.get_id(device_id, ret_object=False)})


@DEVICES.route('<device_id>/channels.json', methods=["GET"])
def device_channels_json(device_id):
    d = device.get_id(device_id, ret_object=True)
    if d:
        return jsonify({'data': channel.get_local_filter(ret_object=False, exten=d.extension)})
    else:
        abort(404)

