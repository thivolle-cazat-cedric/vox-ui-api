# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template
from flask.json import jsonify
from app.voxity import sms
from app.voxity.objects.sms import SmsForm
from app.controllers import is_auth


SMS = Blueprint('SMS', __name__)


@SMS.route('json/', methods=["GET"])
@is_auth
def sms_json():
    return jsonify({'data': sms.get()})


@SMS.route('json/group_by_dest', methods=["GET"])
@is_auth
def sms_gp_by():
    return jsonify({'data': sms.get_group_by_dest()})


@SMS.route('index.html', methods=["GET"])
@is_auth
def index():
    return render_template(
        'sms/index.html',
        container_class="container-fluid",
        sms=sms.get_group_by_dest(ret_object=True)
    )


@SMS.route('new.html', methods=["GET"])
@is_auth
def new():
    return render_template(
        'sms/form.html',
        form=SmsForm()
    )
