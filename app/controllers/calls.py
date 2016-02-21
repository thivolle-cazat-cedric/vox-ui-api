# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, request, abort
from flask.json import jsonify
from app.controllers import is_auth
from app import voxity


CALLS = Blueprint('CALLS', __name__)


@CALLS.route('generate', methods=["POST"])
@is_auth
def generate_call():
    if 'exten' in request.form:
        resp = voxity.call(request.form['exten'])
        if resp.get('status', False):
            if str(resp['status']) == "1":
                return jsonify({'data': resp})
            elif str(resp['status']) == "500":
                return jsonify({'data': resp})
            else:
                return jsonify({'data': resp}), 400

    abort(500)
