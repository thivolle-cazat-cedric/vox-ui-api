# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint
from flask.json import jsonify
from app import voxity

CALLS = Blueprint('CALLS', __name__)


@CALLS.route('generate', methods=["GET"])
def generate_call():
    return jsonify({'data': voxity.call('0666951941')})
