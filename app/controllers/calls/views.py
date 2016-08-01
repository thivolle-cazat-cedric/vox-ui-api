# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, request, abort
from flask.json import jsonify
from app.controllers import is_auth
from app.voxity import channel


CALLS = Blueprint('CALLS',
    __name__,
    url_prefix='/calls'
)


@CALLS.route('/generate', methods=["POST"])
@is_auth
def generate_call():
    if 'exten' in request.form:
        resp = channel.create(request.form['exten'])
        if resp.get('status', False):
            if str(resp['status']) == "200":
                return jsonify({'data': resp})
            elif str(resp['status']) == "500":
                return jsonify({'data': resp})
            else:
                return jsonify({'data': resp}), 400

    abort(500)


@CALLS.route('/json/', methods=["GET"])
@is_auth
def channels_json():
    filter_query = dict()
    for k in channel.Channel.__ATTR__:
        if request.args.get(k, False):
            filter_query[k] = request.args.get(k)

    return jsonify({'data': channel.get_local_filter(**filter_query)})


@CALLS.route('/<id>.json', methods=["GET"])
@is_auth
def channel_json(id):
    return jsonify({'data': channel.get_id(id)})
