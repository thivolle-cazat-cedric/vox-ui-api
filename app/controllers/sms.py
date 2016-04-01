# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals
from flask import Blueprint, render_template, request
from flask.json import jsonify
from app.voxity import sms
from app.voxity.objects.sms import SmsForm, Sms
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


@SMS.route('new.html', methods=["POST"])
@is_auth
def send():
    sms_form = SmsForm(request.form)
    sms_form.strip_value()
    if sms_form.validate():
        for mess in sms_form.get_object(Sms):
            print(mess)

    return render_template(
        'sms/form.html',
        form=sms_form,
        validate_state=True,
    )
